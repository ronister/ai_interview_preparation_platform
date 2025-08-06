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
import asyncio
from microsandbox import PythonSandbox

from apps.authentication.authentication import JWTOnlyAuthentication
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from .models import UserProgress, UserQuestionAttempt
from .serializers import (
    UserStatsSerializer, QuestionSerializer, CodeSubmissionSerializer,
    CodeExecutionSerializer, GradeFeedbackSerializer, AttemptHistorySerializer
)
from .grading import PythonGradingEngine

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_user_stats(request):
    """Get or create user progress statistics."""
    try:
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3}
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


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def get_next_question(request):
    """Get the next question based on user's current level."""
    try:
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3}
        )
        
        # Get questions at the user's current level
        questions = PythonProgrammingQuestion.objects.filter(
            difficulty_level=user_progress.current_level
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
                user_progress.current_level - 1,
                user_progress.current_level + 1
            ]
            available_questions = PythonProgrammingQuestion.objects.filter(
                difficulty_level__in=[l for l in nearby_levels if 1 <= l <= 5]
            ).exclude(id__in=attempted_question_ids)
        
        if available_questions.exists():
            # Select a random question
            question = random.choice(available_questions)
            serializer = QuestionSerializer(question)
            
            # Include user stats in response
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
    """Submit a solution for grading."""
    serializer = CodeSubmissionSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        question_id = serializer.validated_data['question_id']
        code = serializer.validated_data['code']
        
        # Get the question
        question = PythonProgrammingQuestion.objects.get(id=question_id)
        
        # Get user progress
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            defaults={'current_level': 3}
        )
        
        # Simulate test execution results
        # In a real implementation, this would come from the frontend after Brython execution
        # For now, we'll create mock test results
        test_results = run_test_cases(code, question)
        execution_time = test_results.get('execution_time', 0.1)
        
        # Grade the submission
        grading_engine = PythonGradingEngine()
        grade, feedback = grading_engine.grade_submission(
            code=code,
            expected_output=question.output,
            test_results=test_results,
            execution_time=execution_time
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
        
        # Update user progress
        old_level = user_progress.current_level
        user_progress.total_questions_attempted += 1
        user_progress.total_score += grade
        
        # Increment correct answers count for grades 7-10
        if grade >= 7:
            user_progress.correct_answers_count += 1
        
        user_progress.update_level(grade)
        
        level_changed = old_level != user_progress.current_level
        
        # Prepare response
        response_data = {
            'grade': grade,
            'feedback': feedback,
            'test_results': test_results,
            'execution_time': execution_time,
            'level_changed': level_changed,
            'new_level': user_progress.current_level if level_changed else None
        }
        
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


def run_test_cases(code: str, question: PythonProgrammingQuestion) -> dict:
    """
    Mock function to simulate running test cases.
    In production, this would be replaced with actual test execution
    from the frontend using Brython.
    """
    # This is a simplified mock - the real execution happens in the frontend
    # The frontend will send back the actual test results
    
    # For now, return mock results based on simple heuristics
    has_function = 'def ' in code
    has_return = 'return' in code or 'print' in code
    
    if not has_function or not has_return:
        return {
            'total': 5,
            'passed': 0,
            'failed': 5,
            'execution_time': 0.01,
            'failed_tests': [
                {'name': 'test_basic', 'error': 'No output produced'},
                {'name': 'test_empty', 'error': 'No output produced'},
            ]
        }
    
    # Simulate varying success rates
    import random
    passed = random.randint(2, 5)
    
    return {
        'total': 5,
        'passed': passed,
        'failed': 5 - passed,
        'execution_time': random.uniform(0.01, 0.5),
        'failed_tests': [
            {'name': f'test_{i}', 'error': 'Output mismatch'}
            for i in range(5 - passed)
        ] if passed < 5 else []
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_python_code(request):
    """
    Execute Python code on the backend and return the output without submission (for testing)
    """
    code = request.data.get('code', '').strip()
    if not code:
        return Response({
            'output': '',
            'error': 'No code provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    async def execute_code():
        try:
            async with PythonSandbox.create(name=f"user_{request.user.id}") as sandbox:
                # Set a 10-second timeout for the entire execution
                async with asyncio.timeout(10):
                    exec_result = await sandbox.run(code)
                    output = await exec_result.output()
                    return output, None
        except asyncio.TimeoutError:
            return '', 'Code execution timed out (10 seconds limit)'
        except Exception as e:
            return '', f'Execution error: {str(e)}'
    
    try:
        # Run the async code in the sync Django view
        output, error = asyncio.run(execute_code())
        
        return Response({
            'output': output,
            'error': error,
            'execution_time': datetime.now().isoformat()
        })
    
    except Exception as e:
        return Response({
            'output': '',
            'error': f'Setup error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
