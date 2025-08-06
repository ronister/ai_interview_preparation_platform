import asyncio
from urllib import request
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
import random
import json
import time
import logging
import subprocess
import tempfile
import os
import signal
import sys
from datetime import datetime
import ast
from typing import Tuple

from apps.authentication.authentication import JWTOnlyAuthentication
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from .models import UserProgress, UserQuestionAttempt
from .serializers import (
    UserStatsSerializer, QuestionSerializer, CodeSubmissionSerializer,
    CodeExecutionSerializer, GradeFeedbackSerializer, AttemptHistorySerializer,
    ManualLevelSerializer, LevelChangeSuggestionSerializer
)
from microsandbox import PythonSandbox
from .grading import PythonGradingEngine

logger = logging.getLogger(__name__)

# Flag to choose between execution methods
is_use_microsandbox = False


def execute_python_code(code: str) -> Tuple[str, str, float]:
    """
    Execute Python code using the appropriate method based on is_use_microsandbox flag.
    
    Returns:
        Tuple of (output, error, execution_time)
    """
    if is_use_microsandbox:
        return execute_python_code_with_micro_sandbox(code)
    else:
        return execute_python_code_with_timing(code)


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_user_stats(request):
    """Get or create user progress statistics."""
    try:
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        if created:
            logger.info(f"Created new UserProgress for user: {request.user.username}")
        
        serializer = UserStatsSerializer(user_progress)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return Response(
            {'error': 'Failed to retrieve user statistics'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def set_manual_level(request):
    """Set user's manual difficulty level preference."""
    serializer = ManualLevelSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        level = serializer.validated_data['level']
        
        # Get or create user progress
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Set the manual level
        success = user_progress.set_manual_level(level)
        
        if success:
            # Return updated user stats
            stats_serializer = UserStatsSerializer(user_progress)
            return Response({
                'message': f'Manual level set to {level}',
                'user_stats': stats_serializer.data
            })
        else:
            return Response(
                {'error': 'Invalid level value'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        logger.error(f"Error setting manual level: {e}")
        return Response(
            {'error': 'Failed to set manual level'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_next_question(request):
    """Get the next question based on user's manual level preference."""
    try:
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Check if user has a current question assigned
        if user_progress.current_question:
            # Return the current question
            serializer = QuestionSerializer(user_progress.current_question)
            stats_serializer = UserStatsSerializer(user_progress)
            
            logger.info(f"Returning current assigned question {user_progress.current_question.id} to user {request.user.username}")
            
            return Response({
                'question': serializer.data,
                'user_stats': stats_serializer.data
            })
        
        # No current question, assign a new one
        effective_level = user_progress.get_effective_level()
        
        # Get questions at the user's effective level
        questions = PythonProgrammingQuestion.objects.filter(
            difficulty_level=effective_level
        )
        
        # Get IDs of questions the user has already attempted
        attempted_question_ids = UserQuestionAttempt.objects.filter(
            user=request.user
        ).values_list('question_id', flat=True)
        
        # Filter out attempted questions
        available_questions = questions.exclude(id__in=attempted_question_ids)
        
        # If no new questions at current level, get any question at that level
        if not available_questions.exists():
            available_questions = questions
        
        # If still no questions, expand to nearby levels
        if not available_questions.exists():
            nearby_levels = [
                effective_level - 1,
                effective_level + 1
            ]
            available_questions = PythonProgrammingQuestion.objects.filter(
                difficulty_level__in=[l for l in nearby_levels if 1 <= l <= 5]
            ).exclude(id__in=attempted_question_ids)
        
        if available_questions.exists():
            # Select a random question
            question = random.choice(available_questions)
            
            # Assign the question to the user
            user_progress.assign_question(question)
            
            logger.info(f"Assigned new question {question.id} to user {request.user.username}")
            
            serializer = QuestionSerializer(question)
            stats_serializer = UserStatsSerializer(user_progress)
            
            return Response({
                'question': serializer.data,
                'user_stats': stats_serializer.data
            })
        else:
            return Response(
                {'error': 'No questions available at your level'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        logger.error(f"Error getting next question: {e}")
        return Response(
            {'error': 'Failed to retrieve next question'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def submit_solution(request):
    logger.info(f"Submitting solution for user {request.user.username}")
    """Submit a solution for grading."""
    serializer = CodeSubmissionSerializer(data=request.data)
    logger.debug(f"DEBUG: Serializer created successfully, valid: {serializer.is_valid()}")
    
    if not serializer.is_valid():
        logger.error(f"DEBUG: Serializer validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        question_id = serializer.validated_data['question_id']
        code = serializer.validated_data['code']
        logger.debug(f"DEBUG: Extracted question_id={question_id}, code_length={len(code)}, code_preview='{code[:50]}...'")
        
        # Get the question
        question = PythonProgrammingQuestion.objects.get(id=question_id)
        
        # Get user progress
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Validate that the user is submitting their currently assigned question
        if user_progress.current_question and user_progress.current_question.id != question_id:
            return Response(
                {'error': 'You can only submit the question currently assigned to you'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If no current question is assigned, assign this one (for backward compatibility)
        if not user_progress.current_question:
            user_progress.assign_question(question)
        
        # Execute the code to measure actual execution time
        _, _, execution_time = execute_python_code(code)
        
        # Create empty test_results dict since it's still expected by the grading engine
        # but not actually used in any evaluation
        test_results = {}
        
        # Grade the submission
        grading_engine = PythonGradingEngine()
        grade, feedback = grading_engine.grade_submission(
            code=code,
            question=question,
            test_results=test_results,
            execution_time=execution_time,
            user_id=request.user.id,
            username=request.user.username
        )
        
        # Save the attempt
        attempt = UserQuestionAttempt.objects.create(
            user=request.user,
            question=question,
            submitted_code=code,
            grade=grade,
            execution_time=execution_time,
            test_results=test_results,
            feedback=feedback
        )
        
        # Clear the current question since it's been submitted
        user_progress.clear_current_question()
        
        # Update user progress
        old_level = user_progress.current_level
        user_progress.total_questions_attempted += 1
        user_progress.total_score += grade
        
        # Increment correct answers count for grades 7-10
        if grade >= 7:
            user_progress.correct_answers_count += 1
        
        # Check for level change suggestion before updating counters
        level_suggestion = user_progress.check_level_change_suggestion(grade)
        
        # Update automatic level tracking (but don't use it for questions)
        user_progress.update_level(grade)
        
        level_changed = old_level != user_progress.current_level
        
        # Prepare response
        response_data = {
            'grade': grade,
            'feedback': feedback,
            'test_results': test_results,
            'execution_time': execution_time,
            'level_changed': level_changed,
            'new_level': user_progress.current_level if level_changed else None,
            'level_suggestion': level_suggestion
        }
        
        # Debug logging to verify all feedback is present
        logger.debug(f"Feedback being sent to frontend:")
        logger.debug(f"- Correctness: {feedback.get('correctness', {}).get('message', 'Not found')}")
        logger.debug(f"- Code Quality: {feedback.get('code_quality', {}).get('message', 'Not found')}")
        logger.debug(f"- Efficiency: {feedback.get('efficiency', {}).get('message', 'Not found')}")
        logger.debug(f"- Sophistication: {feedback.get('sophistication', {}).get('message', 'Not found')}")
        logger.debug(f"- Overall: {feedback.get('overall', 'Not found')}")
        
        response_serializer = GradeFeedbackSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data)
        else:
            return Response(response_data)
            
    except PythonProgrammingQuestion.DoesNotExist:
        return Response(
            {'error': 'Question not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error submitting solution: {e}")
        return Response(
            {'error': 'Failed to submit solution'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_attempt_history(request):
    """Get user's attempt history."""
    try:
        attempts = UserQuestionAttempt.objects.filter(
            user=request.user
        ).order_by('-attempted_at')[:20]  # Last 20 attempts
        
        serializer = AttemptHistorySerializer(attempts, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"Error getting attempt history: {e}")
        return Response(
            {'error': 'Failed to retrieve attempt history'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def clear_user_progress(request):
    """Clear all user progress data including UserProgress and UserQuestionAttempt records."""
    try:
        user = request.user
        logger.info(f"Clearing progress for user: {user.username} (ID: {user.id})")
        
        # Delete all UserQuestionAttempt records for this user
        attempts_deleted, _ = UserQuestionAttempt.objects.filter(user=user).delete()
        
        # Clear current question from UserProgress before deleting
        user_progress = UserProgress.objects.filter(user=user).first()
        if user_progress:
            user_progress.clear_current_question()
        
        # Delete UserProgress record for this user (if exists)
        progress_deleted, _ = UserProgress.objects.filter(user=user).delete()
        
        logger.info(f"Cleared progress for user {user.username}: "
                   f"{attempts_deleted} attempts, {progress_deleted} progress records")
        
        return Response({
            'message': 'Clear Progress completed',
            'attempts_cleared': attempts_deleted,
            'progress_cleared': progress_deleted
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error clearing user progress: {e}")
        return Response(
            {'error': 'Failed to clear user progress'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def abandon_current_question(request):
    """Allow user to abandon their current question, recording it as a failed attempt."""
    try:
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3, 'manual_level': 3}
        )
        
        # Check if user has a current question
        if not user_progress.current_question:
            return Response(
                {'error': 'No current question to abandon'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_question = user_progress.current_question
        
        # Record the abandonment as a failed attempt with grade 0
        attempt = UserQuestionAttempt.objects.create(
            user=request.user,
            question=current_question,
            submitted_code="",  # Empty code for abandoned question
            grade=0,  # Grade 0 for abandoned question
            execution_time=0.0,
            test_results={},
            feedback={
                'overall': 'Question abandoned by user',
                'correctness': {'score': 0, 'message': 'Question was abandoned'},
                'code_quality': {'score': 0, 'message': 'No code submitted'},
                'efficiency': {'score': 0, 'message': 'No code submitted'},
                'sophistication': {'score': 0, 'message': 'No code submitted'}
            }
        )
        
        # Update user progress statistics
        old_level = user_progress.current_level
        user_progress.total_questions_attempted += 1
        user_progress.total_score += 0  # Add 0 to score
        
        # Check for level change suggestion
        level_suggestion = user_progress.check_level_change_suggestion(0)
        
        # Update automatic level tracking
        user_progress.update_level(0)
        
        # Clear the current question
        user_progress.clear_current_question()
        
        level_changed = old_level != user_progress.current_level
        
        logger.info(f"User {request.user.username} abandoned question {current_question.id}")
        
        return Response({
            'message': 'Question abandoned successfully',
            'level_changed': level_changed,
            'new_level': user_progress.current_level if level_changed else None,
            'level_suggestion': level_suggestion
        })
        
    except Exception as e:
        logger.error(f"Error abandoning current question: {e}")
        return Response(
            {'error': 'Failed to abandon current question'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_python_code(request):
    """
    Execute Python code on the backend and return the output without submission (for testing)
    """
    code = request.data.get('code', '')
    
    # Execute the code and get output, error, and execution time (empty code is allowed)
    output, error, execution_time = execute_python_code(code)
    
    # Return appropriate response based on error status
    if error and 'timed out' in error:
        return Response({
            'output': output,
            'error': error,
            'execution_time': execution_time
        }, status=status.HTTP_408_REQUEST_TIMEOUT)
    
    return Response({
        'output': output,
        'error': error,
        'execution_time': execution_time
    })

def execute_python_code_with_micro_sandbox(code: str) -> Tuple[str, str, float]:
    """
    Execute Python code using microsandbox and return output, error, and execution time.
    
    Returns:
        Tuple of (output, error, execution_time)
    """
    if os.environ.get('SKIP_CODE_EXECUTION') == 'True':
        return 'Code execution is disabled in this environment', None, 0.1
    
    try:
        # Process the code to handle expressions like REPL
        processed_code = process_code_for_repl(code)
        
        # Measure execution time
        start_time = time.time()
        
        try:
            # Execute using microsandbox with timeout
            async def run_with_sandbox():
                async with PythonSandbox.create(name=f"sandbox_{int(time.time())}") as sandbox:
                    # Set a 10-second timeout for the entire execution
                    async with asyncio.timeout(10):
                        exec_result = await sandbox.run(processed_code)
                        output = await exec_result.output()
                        return output, None
            
            # Run the async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                output, error = loop.run_until_complete(run_with_sandbox())
            finally:
                loop.close()
            
            # Calculate execution time in seconds
            execution_time = time.time() - start_time
            
            return output, error, execution_time
            
        except asyncio.TimeoutError:
            return '', 'Code execution timed out (10 seconds limit)', 10.0
            
    except Exception as e:
        return '', f'Execution error: {str(e)}', 0.1

def execute_python_code_with_timing(code: str) -> Tuple[str, str, float]:
    """
    Execute Python code and return output, error, and execution time.
    
    Returns:
        Tuple of (output, error, execution_time)
    """
    if os.environ.get('SKIP_CODE_EXECUTION') == 'True':
        return 'Code execution is disabled in this environment', None, 0.1
    
    try:
        # Process the code to handle expressions like REPL
        processed_code = process_code_for_repl(code)
        
        # Create a temporary file for the Python code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(processed_code)
            temp_file_path = temp_file.name
        
        try:
            # Measure execution time
            start_time = time.time()
            
            # Execute the Python code with timeout
            result = subprocess.run([
                sys.executable, temp_file_path
            ], 
            capture_output=True, 
            text=True, 
            timeout=10,  # 10 second timeout
            cwd=tempfile.gettempdir()  # Run in temp directory for security
            )
            
            # Calculate execution time in seconds
            execution_time = time.time() - start_time
            
            output = result.stdout
            error = result.stderr if result.returncode != 0 else None
            
            return output, error, execution_time
            
        except subprocess.TimeoutExpired:
            return '', 'Code execution timed out (10 seconds limit)', 10.0
            
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
        return '', f'Execution error: {str(e)}', 0.1


def process_code_for_repl(code: str) -> str:
    """
    Process code to make it behave like a REPL, automatically printing expressions.
    """
    # Handle empty code
    if not code or not code.strip():
        return ''
    
    lines = code.strip().split('\n')
    if not lines:
        return code
    
    try:
        # Try to parse the entire code first
        tree = ast.parse(code)
        
        # If the last statement is an expression, wrap it with print()
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            # Split code into all lines except the last expression
            all_but_last = '\n'.join(lines[:-1])
            last_line = lines[-1].strip()
            
            # Check if the last line is likely an expression (not an assignment or statement)
            try:
                # Parse just the last line
                last_tree = ast.parse(last_line)
                if last_tree.body and isinstance(last_tree.body[0], ast.Expr):
                    # It's an expression, wrap it with conditional print to skip None values
                    if all_but_last.strip():
                        return f"{all_but_last}\n_expr_result = {last_line}\nif _expr_result is not None:\n    print(_expr_result)"
                    else:
                        return f"_expr_result = {last_line}\nif _expr_result is not None:\n    print(_expr_result)"
            except:
                pass
        
        # For single-line expressions
        if len(lines) == 1:
            try:
                # Try to parse as an expression
                ast.parse(lines[0], mode='eval')
                # It's a valid expression, wrap with conditional print
                return f"_expr_result = {lines[0]}\nif _expr_result is not None:\n    print(_expr_result)"
            except:
                # Not a simple expression, return as is
                pass
                
    except SyntaxError:
        # If there's a syntax error, let it fail naturally during execution
        pass
    
    return code
