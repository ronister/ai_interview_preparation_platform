import ast
import re
import json
import math
import logging
from typing import Dict, List, Tuple, Any
from apps.api import ClaudeService
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from langchain.prompts import PromptTemplate
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
grading_logger = logging.getLogger('grading_logger')


class PythonGradingEngine:
    """
    Grades Python code submissions on a scale of 0-10.
    
    Grade 0 is reserved for:
    - Empty code submissions
    - Submissions containing only comments (no executable code)
    
    Grades 1-10 are calculated based on:
    - Correctness (40%): 4 points max
    - Code Quality (30%): 3 points max  
    - Efficiency (20%): 2 points max
    - Sophistication (10%): 1 point max
    """
    
    def __init__(self):
        self.total_points = 10
        self.claude_service = ClaudeService()
        
    def grade_submission(
        self, 
        code: str, 
        question: 'PythonProgrammingQuestion',
        test_results: Dict[str, Any],
        execution_time: float = None,
        user_id: int = None,
        username: str = None
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Grade a code submission and return grade (0-10) and detailed feedback.
        
        Grade 0 is returned for empty code or code with only comments.
        Grades 1-10 are calculated using weighted scoring with ceil function.
        
        Args:
            code: The submitted Python code
            question: The PythonProgrammingQuestion object
            test_results: Results from running test cases
            execution_time: Time taken to execute the code
            user_id: User ID for logging purposes
            username: Username for logging purposes
            
        Returns:
            Tuple of (grade, feedback_dict)
        """
        # Log grading start
        grading_logger.info(f"{'='*80}")
        grading_logger.info(f"GRADING START - User: {username} (ID: {user_id})")
        grading_logger.info(f"Question ID: {question.id}")
        grading_logger.info(f"Question Instruction: {question.instruction}")
        grading_logger.info(f"Question Input: {question.input}")
        grading_logger.info(f"Expected Output: {question.output}")
        grading_logger.info(f"Difficulty Level: {question.difficulty_level}")
        grading_logger.info(f"Execution Time: {execution_time:.3f}s")
        grading_logger.info(f"Submitted Code:\n{code}")
        grading_logger.info(f"{'-'*80}")
        feedback = {
            'correctness': {},
            'code_quality': {},
            'efficiency': {},
            'sophistication': {},
            'overall': ''
        }
        
        # Check for empty code or comments-only code
        if self._is_empty_or_comments_only(code):
            feedback['overall'] = self._generate_overall_feedback(
                0, 0.0, 0.0, 0.0, 0.0, is_empty_or_comments_only=True
            )
            feedback['correctness'] = {'score': 0, 'message': 'No code to evaluate.'}
            feedback['code_quality'] = {'score': 0, 'message': 'No code to evaluate.'}
            feedback['efficiency'] = {'score': 0, 'message': 'No code to evaluate.'}
            feedback['sophistication'] = {'score': 0, 'message': 'No code to evaluate.'}
            
            # Log grade 0 results
            grading_logger.info(f"Empty or comments-only code detected")
            grading_logger.info(f"Correctness Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"Code Quality Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"Efficiency Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"Sophistication Score: 0.00 - No code to evaluate.")
            grading_logger.info(f"{'-'*80}")
            grading_logger.info(f"Weighted Score: 0.0000")
            grading_logger.info(f"Final Grade: 0/10")
            grading_logger.info(f"Overall Feedback: {feedback['overall']}")
            grading_logger.info(f"GRADING END - User: {username} (ID: {user_id})")
            grading_logger.info(f"{'='*80}\n")
            
            return 0, feedback
        
        # Calculate individual scores (0-1 scale)
        correctness_score = self._evaluate_correctness(code, question, feedback)
        grading_logger.info(f"Correctness Score: {correctness_score:.2f} - {feedback['correctness'].get('message', 'No message')}")
        
        # If correctness is zero, all other scores should be zero
        if correctness_score == 0:
            quality_score = 0
            efficiency_score = 0
            sophistication_score = 0
            
            # Set appropriate feedback messages for zero scores
            feedback['code_quality'] = {
                'score': 0,
                'message': 'Code quality cannot be evaluated when correctness is zero.',
                'issues': ['Code must be correct before quality can be assessed']
            }
            feedback['efficiency'] = {
                'score': 0,
                'message': 'Efficiency cannot be evaluated when correctness is zero.',
                'inefficiencies': ['Code must be correct before efficiency can be assessed'],
                'suggestions': []
            }
            feedback['sophistication'] = {
                'score': 0,
                'message': 'Sophistication cannot be evaluated when correctness is zero.',
                'areas_for_improvement': ['Code must be correct before sophistication can be assessed'],
                'advanced_techniques': []
            }
            
            grading_logger.info(f"Code Quality Score: 0.00 - Code quality cannot be evaluated when correctness is zero.")
            grading_logger.info(f"Efficiency Score: 0.00 - Efficiency cannot be evaluated when correctness is zero.")
            grading_logger.info(f"Sophistication Score: 0.00 - Sophistication cannot be evaluated when correctness is zero.")
        else:
            # Normal evaluation for non-zero correctness
            # Code quality can run immediately (no API call)
            quality_score = self._evaluate_code_quality(code, question, feedback)
            grading_logger.info(f"Code Quality Score: {quality_score:.2f} - {feedback['code_quality'].get('message', 'No message')}")
            
            # Run efficiency and sophistication evaluations in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Submit both API calls
                future_efficiency = executor.submit(
                    self._evaluate_efficiency, code, execution_time, question, feedback
                )
                future_sophistication = executor.submit(
                    self._evaluate_sophistication, code, question, feedback
                )
                
                # Wait for both to complete
                efficiency_score = future_efficiency.result()
                sophistication_score = future_sophistication.result()
            
            grading_logger.info(f"Efficiency Score: {efficiency_score:.2f} - {feedback['efficiency'].get('message', 'No message')}")
            grading_logger.info(f"Sophistication Score: {sophistication_score:.2f} - {feedback['sophistication'].get('message', 'No message')}")
        
        # Calculate weighted_score (0-1 scale)
        weighted_score = (
            correctness_score * 0.4 +
            quality_score * 0.3 +
            efficiency_score * 0.2 +
            sophistication_score * 0.1
        )
        
        # Calculate grade (1-10) using ceil function
        # Any positive weighted score results in at least grade 1
        # If all scores are zero, grade should be zero
        if weighted_score > 0:
            grade = math.ceil(weighted_score * 10)
        else:
            grade = 0  # Grade 0 when all aspects score zero
        
        # Generate overall feedback
        feedback['overall'] = self._generate_overall_feedback(
            grade, correctness_score, quality_score, 
            efficiency_score, sophistication_score, 
            is_empty_or_comments_only=False
        )
        
        # Log final results
        grading_logger.info(f"{'-'*80}")
        grading_logger.info(f"Weighted Score: {weighted_score:.4f}")
        grading_logger.info(f"Final Grade: {grade}/10")
        grading_logger.info(f"Overall Feedback: {feedback['overall']}")
        grading_logger.info(f"GRADING END - User: {username} (ID: {user_id})")
        grading_logger.info(f"{'='*80}\n")
        
        return grade, feedback
    
    def _evaluate_correctness(self, code: str, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate correctness using Claude API for static code analysis (0-1 scale)."""
        try:
            # Create prompt for Claude to evaluate correctness
            prompt_template = PromptTemplate(
                input_variables=["code", "instruction", "input", "output"],
                template="""
Please evaluate the correctness of the following Python code submission based on static analysis.

Problem Instruction: {instruction}
Expected Input: {input}
Expected Output: {output}

Submitted Code:
```python
{code}
```

**IMPORTANT GRADING CONSIDERATIONS**:
1. **Function Names**: DO NOT penalize for function name differences. Students cannot see the expected solution, so as long as the function name is meaningful and descriptive of its functionality, it should NOT affect the correctness score.

2. **REPL-like Execution**: The code execution simulates REPL (Read-Eval-Print Loop) behavior. The system automatically wraps the last expression with a print statement if it evaluates to a non-None value. This is EXPECTED behavior and should NOT be penalized. For example:
   - `calculate_sum(5, 3)` at the end will automatically print the result
   - `5 + 3` as the last line will automatically print `8`
   - `my_variable` at the end will print its value (if not None)
   - This is functionally equivalent to having an explicit print() statement

DO NOT mark the code as having "no output" or penalize for "missing print statements" if the solution relies on this automatic printing behavior. The code is correct if the last expression produces the expected output value.

Evaluate the code based on these criteria:

1. **Syntax and Structure Analysis**:
   - Check for proper Python syntax (indentation, colons, parentheses)
   - Verify function definitions include proper parameters and return statements
   - Examine conditional statements for logical completeness
   - Look for proper loop termination conditions

2. **Algorithm Logic Review**:
   - Trace through the code logic manually with sample inputs
   - Verify that the algorithm follows the problem requirements
   - Check for proper variable initialization and usage
   - Examine control flow paths to ensure all scenarios are handled

3. **Correctness Score Guidelines**:
   - 0.8-1.0: Code structure appears sound, logic follows requirements, all major components implemented
   - 0.5-0.7: Some logical issues or missing components, but core functionality present
   - 0.2-0.4: Significant logical flaws or incomplete implementation
   - 0.0-0.1: Major structural problems or completely incorrect approach

Please respond in JSON format:
{{
    "score": <float between 0 and 1>,
    "analysis": "<detailed explanation of your analysis>",
    "issues": ["<list of specific issues found, if any>"],
    "strengths": ["<list of strengths in the implementation>"]
}}
"""
            )
            
            prompt = prompt_template.format(
                code=code,
                instruction=question.instruction,
                input=question.input,
                output=question.output
            )
            # ...

            # Call Claude API
            response_text = self.claude_service.send_message(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Try to extract JSON from response
            import json
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = {
                        "score": 0.5,
                        "analysis": response_text,
                        "issues": ["Could not parse evaluation"],
                        "strengths": []
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "score": 0.5,
                    "analysis": response_text,
                    "issues": ["Could not parse evaluation"],
                    "strengths": []
                }
            
            score = float(result.get('score', 0.5))
            score = max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
            
            # Log Claude API analysis
            grading_logger.debug(f"Correctness Analysis: {result.get('analysis', 'No analysis')}")
            if result.get('issues'):
                grading_logger.debug(f"Issues Found: {result.get('issues', [])}")
            if result.get('strengths'):
                grading_logger.debug(f"Strengths: {result.get('strengths', [])}")
            
            # Generate feedback message
            if score >= 0.9:
                message = f"Excellent! Your code logic appears correct and well-structured."
            elif score >= 0.7:
                message = f"Good job! Your code shows solid understanding with minor issues."
            elif score >= 0.5:
                message = f"Partial success. Your code has the right idea but needs improvements."
            elif score >= 0.3:
                message = f"Keep trying! Your code has some logical issues that need fixing."
            else:
                message = f"Review the problem requirements carefully and restructure your approach."
            
            # Don't add specific feedback to message - it will be shown in sub-bullets
            
            feedback['correctness'] = {
                'score': score,
                'message': message,
                'analysis': result.get('analysis', ''),
                'issues': result.get('issues', []),
                'strengths': result.get('strengths', [])
            }
            
            return score
            
        except Exception as e:
            # Fallback if API call fails
            logger.error(f"Error evaluating correctness with Claude API: {e}")
            feedback['correctness'] = {
                'score': 0.5,
                'message': 'Could not evaluate correctness automatically. Manual review recommended.',
                'error': str(e)
            }
            return 0.5
    
    def _evaluate_code_quality(self, code: str, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate code quality (0-1 scale) adjusted for difficulty level."""
        quality_score = 1.0
        issues = []
        difficulty_level = question.difficulty_level
        
        try:
            # Parse the code AST
            tree = ast.parse(code)
            
            # Check for functions (only for appropriate difficulty levels)
            if difficulty_level >= 2:  # Only expect functions for Easy and above
                functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                if not functions and len(code.split('\n')) > 10:  # Only penalize if code is long enough to warrant functions
                    if difficulty_level == 2:
                        quality_score -= 0.1  # Smaller penalty for Easy level
                        issues.append("Consider using functions to organize your code")
                    else:
                        quality_score -= 0.2  # Larger penalty for Medium and above
                        issues.append("Use functions to organize your code better")
            
            # Check for meaningful variable names (adjusted by level)
            if self._has_poor_variable_names(code):
                if difficulty_level == 1:
                    quality_score -= 0.1  # Smaller penalty for beginners
                    issues.append("Try to use more descriptive variable names")
                else:
                    quality_score -= 0.2
                    issues.append("Use more descriptive variable names")
            
            # Check for comments (only for appropriate difficulty levels)
            if difficulty_level >= 2:  # Don't expect comments for very basic problems
                if code.count('#') < 1 and code.count('"""') < 1 and len(code.split('\n')) > 5:
                    quality_score -= 0.1
                    issues.append("Add comments to explain your logic")
            
            # Check line length (less strict for beginners)
            if difficulty_level >= 3:
                long_lines = [line for line in code.split('\n') if len(line) > 80]
                if len(long_lines) > 3:
                    quality_score -= 0.1
                    issues.append("Some lines are too long (>80 characters)")
            else:
                # More lenient for beginners
                long_lines = [line for line in code.split('\n') if len(line) > 100]
                if len(long_lines) > 5:
                    quality_score -= 0.05
                    issues.append("Try to keep lines shorter for better readability")
            
            # Check for duplicate code (adjusted by level)
            if self._has_duplicate_code(code):
                if difficulty_level >= 2:
                    quality_score -= 0.2
                    issues.append("Avoid code duplication - use functions or loops")
                else:
                    quality_score -= 0.1
                    issues.append("Try to avoid repeating the same code")
                
        except SyntaxError:
            quality_score = 0.1
            issues = ["Syntax error in code"]
        
        quality_score = max(0, quality_score)
        
        # Generate level-appropriate feedback messages
        if difficulty_level == 1:  # Very Easy
            if quality_score >= 0.9:
                message = "Great code quality for a beginner problem!"
            elif quality_score >= 0.7:
                message = "Good code quality. Keep practicing!"
            else:
                message = "Your code works but could be cleaner."
        elif difficulty_level == 2:  # Easy
            if quality_score >= 0.9:
                message = "Excellent code quality! Well organized."
            elif quality_score >= 0.7:
                message = "Good code quality. Consider the suggestions."
            else:
                message = "Code quality needs some improvement."
        else:  # Medium and above
            if quality_score >= 0.9:
                message = "Excellent code quality!"
            elif quality_score >= 0.7:
                message = "Good code quality."
            else:
                message = "Code quality needs improvement."
        
        feedback['code_quality'] = {
            'score': quality_score,
            'issues': issues,
            'message': message
        }
        
        return quality_score
    
    def _evaluate_efficiency(self, code: str, execution_time: float, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate code efficiency using Claude API for context-aware assessment (0-1 scale)."""
        try:
            # Get difficulty level from question
            difficulty_level = question.difficulty_level
            
            # Create prompt for Claude to evaluate efficiency
            prompt_template = PromptTemplate(
                input_variables=["code", "instruction", "input", "output", "difficulty_level"],
                template="""
Please evaluate the efficiency of the following Python code submission based on static performance analysis.

Problem Instruction: {instruction}
Expected Input: {input}
Expected Output: {output}
Difficulty Level: {difficulty_level} (1=Very Easy, 2=Easy, 3=Medium, 4=Hard, 5=Very Hard)

Submitted Code:
```python
{code}
```

**Efficiency Assessment (20% weight) - Static Performance Analysis**

**IMPORTANT: Adjust efficiency expectations based on the difficulty level.**

**Level-Specific Efficiency Guidelines:**

**Level 1 (Very Easy)**: For basic problems:
- Simple, direct solutions are PERFECTLY FINE
- DO NOT penalize for using simple loops when appropriate
- DO NOT expect optimizations like sets or dictionaries
- Focus: Does the code avoid obviously wasteful operations?

**Level 2 (Easy)**: For fundamental problems:
- Basic efficiency awareness (avoiding unnecessary loops)
- Simple optimizations are good but not required
- DO NOT penalize for not using advanced data structures
- Focus: Are there obvious inefficiencies that a beginner should avoid?

**Level 3 (Medium)**: For intermediate problems:
- Expect awareness of time complexity
- Appropriate data structure choices (lists vs sets vs dicts)
- Basic algorithm optimization
- Focus: Is the algorithm choice reasonable for the problem?

**Level 4 (Hard)**: For advanced problems:
- Expect optimal algorithm selection
- Advanced data structure usage
- Consideration of space-time tradeoffs
- Focus: Is this an efficient solution for production code?

**Level 5 (Very Hard)**: For expert problems:
- Expect professional-level optimization
- Advanced algorithmic techniques
- Consideration of real-world constraints
- Focus: Is this optimized for scale and performance?

**General Evaluation Criteria:**

1. **Algorithm Complexity Assessment**:
   - Time Complexity Analysis: Count nested loops, recursive calls
   - Single loops: O(n) - generally efficient
   - Nested loops: O(n²) - acceptable for small datasets
   - Triple nesting or higher: potentially inefficient

2. **Specific Efficiency Indicators to Penalize (adjust severity by level)**:
   - **Excessive Nested Loops**: Only penalize if exceeding what's needed for the problem AND the difficulty level
   - **'in' operator inside loops**: Only penalize at level 3+ and if it significantly impacts performance
   - Inefficient data structure choices: Only penalize at level 3+ 
   - Redundant computations: Severity depends on difficulty level
   - Excessive string concatenation in loops: Only penalize if severe

3. **Efficiency Bonuses (only for appropriate difficulty levels)**:
   - **Efficient Data Structures**: Only bonus at level 3+
   - Smart algorithmic choices: Bonus scaled by difficulty level
   - Space-time tradeoff awareness: Only at level 4+

4. **Context-Aware Evaluation**:
   - Consider the problem's requirements and expected input size
   - DO NOT over-penalize simple solutions for simple problems
   - DO NOT expect advanced optimizations for beginner problems

**Efficiency Scoring Guidelines by Level**:

Level 1-2 (Very Easy/Easy):
- 0.8-1.0: Direct solution without obviously wasteful operations
- 0.5-0.7: Some unnecessary operations but functional
- 0.0-0.4: Clearly inefficient even for a beginner

Level 3 (Medium):
- 0.8-1.0: Good algorithm choice with appropriate data structures
- 0.5-0.7: Reasonable approach with minor inefficiencies
- 0.0-0.4: Poor algorithm choice or significant inefficiencies

Level 4-5 (Hard/Very Hard):
- 0.8-1.0: Optimal or near-optimal implementation
- 0.5-0.7: Good approach with optimization opportunities
- 0.0-0.4: Suboptimal approach for this complexity level

Please respond in JSON format:
{{
    "score": <float between 0 and 1>,
    "analysis": "<detailed explanation appropriate to difficulty level>",
    "time_complexity": "<estimated time complexity e.g. O(n), O(n²)>",
    "inefficiencies": ["<list of level-appropriate inefficiencies, if any>"],
    "suggestions": ["<list of level-appropriate optimization suggestions>"],
    "penalties_applied": ["<list of penalties appropriate to difficulty level>"],
    "bonuses_applied": ["<list of bonuses if appropriate for level>"]
}}
"""
            )
            prompt = prompt_template.format(
                code=code,
                instruction=question.instruction,
                input=question.input,
                output=question.output,
                difficulty_level=difficulty_level
            )
            # ...
            
            # Call Claude API
            response_text = self.claude_service.send_message(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Try to extract JSON from response
            import json
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = {
                        "score": 0.5,
                        "analysis": response_text,
                        "time_complexity": "Unknown",
                        "inefficiencies": ["Could not parse evaluation"],
                        "suggestions": [],
                        "penalties_applied": [],
                        "bonuses_applied": []
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "score": 0.5,
                    "analysis": response_text,
                    "time_complexity": "Unknown",
                    "inefficiencies": ["Could not parse evaluation"],
                    "suggestions": [],
                    "penalties_applied": [],
                    "bonuses_applied": []
                }
            
            score = float(result.get('score', 0.5))
            score = max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
            
            # Log Claude API analysis
            grading_logger.debug(f"Efficiency Analysis: {result.get('analysis', 'No analysis')}")
            grading_logger.debug(f"Time Complexity: {result.get('time_complexity', 'Unknown')}")
            if result.get('inefficiencies'):
                grading_logger.debug(f"Inefficiencies: {result.get('inefficiencies', [])}")
            if result.get('suggestions'):
                grading_logger.debug(f"Optimization Suggestions: {result.get('suggestions', [])}")
            if result.get('penalties_applied'):
                grading_logger.debug(f"Penalties Applied: {result.get('penalties_applied', [])}")
            if result.get('bonuses_applied'):
                grading_logger.debug(f"Bonuses Applied: {result.get('bonuses_applied', [])}")
            
            # Generate feedback message
            if score >= 0.8:
                message = f"Highly efficient solution! Time complexity: {result.get('time_complexity', 'N/A')}."
            elif score >= 0.5:
                message = f"Reasonable efficiency. Time complexity: {result.get('time_complexity', 'N/A')}."
            elif score >= 0.2:
                message = f"Some inefficiencies present. Time complexity: {result.get('time_complexity', 'N/A')}."
            else:
                message = f"Efficiency needs improvement. Time complexity: {result.get('time_complexity', 'N/A')}."
            
            # Don't add specific feedback to message - it will be shown in sub-bullets
            
            feedback['efficiency'] = {
                'score': score,
                'message': message,
                'analysis': result.get('analysis', ''),
                'time_complexity': result.get('time_complexity', 'Unknown'),
                'inefficiencies': result.get('inefficiencies', []),
                'suggestions': result.get('suggestions', []),
                'penalties_applied': result.get('penalties_applied', []),
                'bonuses_applied': result.get('bonuses_applied', [])
            }
            
            return score
            
        except Exception as e:
            # Fallback if API call fails
            logger.error(f"Error evaluating efficiency with Claude API: {e}")
            feedback['efficiency'] = {
                'score': 0.5,
                'message': 'Could not evaluate efficiency automatically. Manual review recommended.',
                'error': str(e)
            }
            return 0.5
    
    def _evaluate_sophistication(self, code: str, question: PythonProgrammingQuestion, feedback: Dict) -> float:
        """Evaluate code sophistication including edge case handling using Claude API (0-1 scale)."""
        try:
            # Get difficulty level from question
            difficulty_level = question.difficulty_level
            
            # Create prompt for Claude to evaluate sophistication
            prompt_template = PromptTemplate(
                input_variables=["code", "instruction", "input", "output", "difficulty_level"],
                template="""
Please evaluate the sophistication of the following Python code submission based on static analysis.

Problem Instruction: {instruction}
Expected Input: {input}
Expected Output: {output}
Difficulty Level: {difficulty_level} (1=Very Easy, 2=Easy, 3=Medium, 4=Hard, 5=Very Hard)

Submitted Code:
```python
{code}
```

**IMPORTANT: Adjust your sophistication expectations based on the difficulty level of the question.**

Code sophistication should be evaluated relative to what's reasonable for the difficulty level:

**Level 1 (Very Easy - Beginner)**: For basic syntax problems, sophistication means:
- Clean, readable code with meaningful variable names (e.g., 'counter' instead of 'i' when appropriate)
- Basic code organization (not everything in one line unless appropriate)
- Simple comments for clarity (if the problem warrants it)
- DO NOT expect: functions, classes, error handling, advanced features, or over-engineering
- Example improvements: Better variable names, simple comments, clean formatting

**Level 2 (Easy - Fundamental)**: For basic programming problems, sophistication means:
- Using functions for code organization (when appropriate)
- Basic input validation for obvious edge cases
- Clear variable and function names
- Basic documentation/comments
- DO NOT expect: OOP, advanced patterns, complex error handling, generators
- Example improvements: Function usage, basic validation, simple docstrings

**Level 3 (Medium - Intermediate)**: For intermediate problems, sophistication means:
- Good use of Python features (list comprehensions, appropriate data structures)
- Proper error handling for common cases
- Well-structured code with clear separation of concerns
- Some consideration of efficiency
- DO NOT expect: Design patterns, async programming, advanced OOP
- Example improvements: List comprehensions, try-except blocks, better algorithms

**Level 4 (Hard - Advanced)**: For complex problems, sophistication means:
- Appropriate use of OOP or functional programming concepts
- Comprehensive error handling
- Good algorithm choices and data structures
- Clear architecture and design
- Edge case handling
- Example improvements: Class design, advanced data structures, optimization

**Level 5 (Very Hard - Expert)**: For professional-level problems, sophistication means:
- Professional-grade code architecture
- Advanced Python features (decorators, generators, async)
- Comprehensive testing considerations
- Performance optimization
- Design patterns where appropriate
- Example improvements: Architecture patterns, advanced optimizations, scalability

**Evaluation Guidelines**:
- Award points for sophistication APPROPRIATE TO THE DIFFICULTY LEVEL
- DO NOT penalize beginners for not using advanced features
- DO NOT suggest over-engineering simple problems
- Focus on what would be the NEXT reasonable improvement for someone at that level

**Sophistication Scoring Based on Difficulty Level**:

For Level 1 (Very Easy):
- 0.8-1.0: Clean, readable code with good variable names and basic organization
- 0.5-0.7: Functional but could use better naming or organization
- 0.0-0.4: Poor organization, unclear variable names, or unnecessarily complex

For Level 2 (Easy):
- 0.8-1.0: Well-organized with functions, basic validation, clear naming
- 0.5-0.7: Some organization, missing some basic best practices
- 0.0-0.4: No functions where needed, poor structure, no validation

For Level 3 (Medium):
- 0.8-1.0: Good use of Python features, proper error handling, efficient approach
- 0.5-0.7: Some advanced features used, basic error handling
- 0.0-0.4: Missing opportunities for Python features, no error handling

For Level 4 (Hard):
- 0.8-1.0: Strong architecture, comprehensive error handling, optimal algorithms
- 0.5-0.7: Good structure, some advanced concepts, decent error handling
- 0.0-0.4: Weak architecture, minimal error handling, suboptimal approach

For Level 5 (Very Hard):
- 0.8-1.0: Professional-grade code with advanced features and optimization
- 0.5-0.7: Good implementation with some advanced concepts
- 0.0-0.4: Basic implementation lacking professional considerations

Please respond in JSON format:
{{
    "score": <float between 0 and 1>,
    "analysis": "<detailed explanation appropriate to the difficulty level>",
    "advanced_techniques": ["<list of techniques used that are appropriate for this level>"],
    "edge_cases_handled": ["<list of edge cases handled, if expected at this level>"],
    "areas_for_improvement": ["<list of LEVEL-APPROPRIATE improvements>"]
}}
"""
            )
            prompt = prompt_template.format(
                code=code,
                instruction=question.instruction,
                input=question.input,
                output=question.output,
                difficulty_level=difficulty_level
            )
            # ...
            
            # Call Claude API
            response_text = self.claude_service.send_message(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Try to extract JSON from response
            import json
            try:
                # Look for JSON in the response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = {
                        "score": 0.5,
                        "analysis": response_text,
                        "advanced_techniques": [],
                        "edge_cases_handled": [],
                        "areas_for_improvement": ["Could not parse evaluation"]
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "score": 0.5,
                    "analysis": response_text,
                    "advanced_techniques": [],
                    "edge_cases_handled": [],
                    "areas_for_improvement": ["Could not parse evaluation"]
                }
            
            score = float(result.get('score', 0.5))
            score = max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
            
            # Log Claude API analysis
            grading_logger.debug(f"Sophistication Analysis: {result.get('analysis', 'No analysis')}")
            if result.get('advanced_techniques'):
                grading_logger.debug(f"Techniques Used: {result.get('advanced_techniques', [])}")
            if result.get('edge_cases_handled'):
                grading_logger.debug(f"Edge Cases Handled: {result.get('edge_cases_handled', [])}")
            if result.get('areas_for_improvement'):
                grading_logger.debug(f"Areas for Improvement: {result.get('areas_for_improvement', [])}")
            
            # Generate feedback message based on difficulty level
            if difficulty_level == 1:  # Very Easy
                if score >= 0.8:
                    message = "Excellent! Your code is clean, readable, and well-organized for a beginner problem."
                elif score >= 0.5:
                    message = "Good job! Your code works well. Consider using more descriptive variable names."
                else:
                    message = "Your solution works, but could be cleaner. Focus on readability and organization."
            elif difficulty_level == 2:  # Easy
                if score >= 0.8:
                    message = "Great work! Your code is well-structured with good use of functions and basic best practices."
                elif score >= 0.5:
                    message = "Good effort! Consider organizing your code with functions and adding basic validation."
                else:
                    message = "Your code works but needs better structure. Try using functions to organize your logic."
            elif difficulty_level == 3:  # Medium
                if score >= 0.8:
                    message = "Excellent! You've used Python features effectively with good error handling and structure."
                elif score >= 0.5:
                    message = "Good implementation! Consider using more Python features like list comprehensions or better error handling."
                else:
                    message = "Your solution could benefit from Python's built-in features and better error handling."
            elif difficulty_level == 4:  # Hard
                if score >= 0.8:
                    message = "Outstanding! Your code shows strong architecture, comprehensive error handling, and optimal design."
                elif score >= 0.5:
                    message = "Good advanced implementation! Consider improving error handling or algorithm optimization."
                else:
                    message = "For this complexity level, focus on better architecture and comprehensive error handling."
            else:  # Level 5 - Very Hard
                if score >= 0.8:
                    message = "Professional-grade code! Excellent use of advanced features and optimization."
                elif score >= 0.5:
                    message = "Strong implementation! Consider additional optimizations or advanced Python features."
                else:
                    message = "For expert-level problems, focus on professional patterns and performance optimization."

            # Don't add specific feedback to message - it will be shown in sub-bullets
            
            feedback['sophistication'] = {
                'score': score,
                'message': message,
                'analysis': result.get('analysis', ''),
                'advanced_techniques': result.get('advanced_techniques', []),
                'edge_cases_handled': result.get('edge_cases_handled', []),
                'areas_for_improvement': result.get('areas_for_improvement', [])
            }
            
            return score
            
        except Exception as e:
            # Fallback if API call fails
            logger.error(f"Error evaluating sophistication with Claude API: {e}")
            feedback['sophistication'] = {
                'score': 0.5,
                'message': 'Could not evaluate sophistication automatically. Manual review recommended.',
                'error': str(e)
            }
            return 0.5
    
    def _generate_overall_feedback(
        self, grade: int, correctness: float, quality: float, 
        efficiency: float, sophistication: float, is_empty_or_comments_only: bool = False
    ) -> str:
        """Generate overall feedback message based on scores."""
        if grade == 0:
            if is_empty_or_comments_only:
                return "No executable code submitted. Please write actual code to solve the problem."
            else:
                return "Your solution is incorrect. Please review the feedback and try again."
        elif grade >= 9:
            return "Outstanding work! Your solution is correct, well-written, and efficient. Keep it up!"
        elif grade >= 7:
            return "Great job! Your solution works well. Check the feedback for minor improvements."
        elif grade >= 5:
            return "Good effort! Your solution partially works. Review the feedback to improve."
        elif grade >= 3:
            return "Keep trying! Focus on getting the basic solution working first, then optimize."
        else:
            return "Don't give up! Review the problem carefully and try a simpler approach first."
    
    def _has_poor_variable_names(self, code: str) -> bool:
        """Check for poor variable naming conventions."""
        # Look for single letter variables (except common ones like i, j for loops)
        poor_names = re.findall(r'\b[a-z]\b(?!\s*in\s+)', code)
        # Exclude common loop variables and function parameters
        poor_names = [n for n in poor_names if n not in ['i', 'j', 'k', 'n', 'm', 'x', 'y']]
        return len(poor_names) > 3
    
    def _has_duplicate_code(self, code: str) -> bool:
        """Simple check for duplicate code patterns."""
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        # Check for duplicate lines (excluding very short lines)
        meaningful_lines = [line for line in lines if len(line) > 10]
        return len(meaningful_lines) != len(set(meaningful_lines))
    
    def _count_nested_loops(self, tree: ast.AST) -> int:
        """Count maximum nesting depth of loops."""
        max_depth = 0
        
        def count_depth(node, depth=0):
            nonlocal max_depth
            if isinstance(node, (ast.For, ast.While)):
                depth += 1
                max_depth = max(max_depth, depth)
            for child in ast.iter_child_nodes(node):
                count_depth(child, depth)
        
        count_depth(tree)
        return max_depth
    
    def _is_empty_or_comments_only(self, code: str) -> bool:
        """Check if code is empty or contains only comments."""
        if not code or not code.strip():
            return True
        
        # Remove all comments and docstrings
        lines = code.split('\n')
        non_comment_lines = []
        in_multiline_string = False
        multiline_delimiter = None
        
        for line in lines:
            stripped = line.strip()
            
            # Handle multiline strings/docstrings
            if not in_multiline_string:
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    multiline_delimiter = '"""' if stripped.startswith('"""') else "'''"
                    if stripped.count(multiline_delimiter) == 1:
                        in_multiline_string = True
                    continue
            else:
                if multiline_delimiter in stripped:
                    in_multiline_string = False
                    multiline_delimiter = None
                continue
            
            # Skip single-line comments
            if stripped.startswith('#'):
                continue
                
            # Skip empty lines
            if not stripped:
                continue
                
            # If we get here, it's a non-comment line
            non_comment_lines.append(line)
        
        # Check if all remaining lines are empty
        remaining_code = '\n'.join(non_comment_lines).strip()
        return len(remaining_code) == 0 