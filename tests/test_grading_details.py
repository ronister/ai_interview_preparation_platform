#!/usr/bin/env python
"""Detailed test to understand grading breakdown."""

import os
import sys
import django

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from apps.practice.grading import PythonGradingEngine
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion

def test_detailed_grading():
    """Test grading with detailed breakdown."""
    engine = PythonGradingEngine()
    
    # Create a mock question
    mock_question = type('MockQuestion', (), {
        'instruction': 'Test instruction',
        'input': 'Test input',
        'output': 'Test output'
    })()
    
    # Test minimal code
    code = 'x = 1'
    
    # Mock test results - all tests fail
    mock_test_results = {
        'total': 5,
        'passed': 0,
        'failed': 5,
        'execution_time': 0.1,
        'failed_tests': []
    }
    
    print("Testing minimal code: 'x = 1'")
    print("All tests fail (0/5 passed)\n")
    
    grade, feedback = engine.grade_submission(
        code=code,
        question=mock_question,
        test_results=mock_test_results,
        execution_time=0.1
    )
    
    print(f"Grade: {grade}")
    print("\nDetailed scores:")
    print(f"Correctness: {feedback['correctness'].get('score', 0):.2f} (weight: 0.4)")
    print(f"Code Quality: {feedback['code_quality'].get('score', 0):.2f} (weight: 0.3)")
    print(f"Efficiency: {feedback['efficiency'].get('score', 0):.2f} (weight: 0.2)")
    print(f"Sophistication: {feedback['sophistication'].get('score', 0):.2f} (weight: 0.1)")
    
    # Calculate weighted score manually
    weighted = (
        feedback['correctness'].get('score', 0) * 0.4 +
        feedback['code_quality'].get('score', 0) * 0.3 +
        feedback['efficiency'].get('score', 0) * 0.2 +
        feedback['sophistication'].get('score', 0) * 0.1
    )
    print(f"\nWeighted score: {weighted:.4f}")
    print(f"Expected grade (ceil({weighted:.4f} * 10)): {int(weighted * 10) + (1 if (weighted * 10) % 1 > 0 else 0)}")
    
    # Test with syntax error
    print("\n" + "="*50)
    print("\nTesting code with syntax error:")
    bad_code = 'def test(\n    return'
    
    grade2, feedback2 = engine.grade_submission(
        code=bad_code,
        question=mock_question,
        test_results=mock_test_results,
        execution_time=0.1
    )
    
    print(f"Grade: {grade2}")
    print(f"Code Quality score: {feedback2['code_quality'].get('score', 0):.2f}")

if __name__ == '__main__':
    test_detailed_grading() 