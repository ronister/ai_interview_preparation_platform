#!/usr/bin/env python
"""Test script to verify grading changes for grade 0 implementation."""

import os
import sys
import django

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project root to the Python path
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from apps.practice.grading import PythonGradingEngine

def test_grading_engine():
    """Test the grading engine with various code submissions."""
    engine = PythonGradingEngine()
    
    # Test cases
    test_cases = [
        {
            'name': 'Empty code',
            'code': '',
            'expected_grade': 0
        },
        {
            'name': 'Only whitespace',
            'code': '   \n\t  \n   ',
            'expected_grade': 0
        },
        {
            'name': 'Only single-line comments',
            'code': '# This is a comment\n# Another comment',
            'expected_grade': 0
        },
        {
            'name': 'Only multi-line comments',
            'code': '"""\nThis is a docstring\n"""\n# And a comment',
            'expected_grade': 0
        },
        {
            'name': 'Minimal code (should get grade 1)',
            'code': 'x = 1',
            'expected_grade': 1
        },
        {
            'name': 'Code with comments',
            'code': '# This is a comment\nx = 1  # inline comment',
            'expected_grade': 1
        },
        {
            'name': 'Function with no tests passing',
            'code': 'def solution():\n    return None',
            'expected_grade': 1
        }
    ]
    
    # Mock test results for non-empty code
    mock_test_results = {
        'total': 5,
        'passed': 0,
        'failed': 5,
        'execution_time': 0.1,
        'failed_tests': []
    }
    
    print("Testing grading engine with new grade 0 logic:\n")
    
    for test in test_cases:
        grade, feedback = engine.grade_submission(
            code=test['code'],
            expected_output='',
            test_results=mock_test_results,
            execution_time=0.1
        )
        
        status = "✓" if grade == test['expected_grade'] else "✗"
        print(f"{status} {test['name']}: Expected grade {test['expected_grade']}, got grade {grade}")
        
        if grade != test['expected_grade']:
            print(f"  Feedback: {feedback.get('overall', 'No overall feedback')}")
    
    print("\nTesting ceil function behavior:")
    # Test ceil function with different weighted scores
    test_scores = [0.0001, 0.1, 0.11, 0.49, 0.5, 0.91, 0.99]
    for score in test_scores:
        # Simulate non-empty code with a specific weighted score
        # We need to manipulate the grading internals for this test
        expected_grade = int(score * 10) + (1 if (score * 10) % 1 > 0 else 0)
        if score == 0:
            expected_grade = 1  # Minimum for non-empty code
        print(f"  Weighted score {score:.4f} should give grade {expected_grade}")

if __name__ == '__main__':
    test_grading_engine() 