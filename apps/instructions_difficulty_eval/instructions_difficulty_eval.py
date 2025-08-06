#!/usr/bin/env python3
"""
Instructions Difficulty Evaluation Script

This script evaluates the difficulty of Python programming questions using Claude API
and saves the results to a PostgreSQL database using Django ORM.

Usage:
    python instructions_difficulty_eval.py

Make sure to set the CLAUDE_API_KEY in your env/.env file before running.
"""

CSV_FILE_PATH = "data/Python Programming Questions Dataset.csv"
SAMPLE_SIZE = 500

# CSV_FILE_PATH = "data/sample_questions.csv"
# SAMPLE_SIZE = 5

import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_interview_preparation_platform.settings")
django.setup()

from difficulty_evaluator import DifficultyEvaluator

def main():
    """
    Main function to run the difficulty evaluation process.
    """
    print("="*60)
    print("PYTHON PROGRAMMING QUESTIONS DIFFICULTY EVALUATION")
    print("="*60)
    print("This script will:")
    print(f"1. Load {SAMPLE_SIZE} random questions from the CSV dataset")
    print("2. Evaluate each question's difficulty using Claude API")
    print("3. Save results to PostgreSQL database")
    print("="*60)
    
    # Check if Claude API key is set
    if not os.getenv('CLAUDE_API_KEY') or os.getenv('CLAUDE_API_KEY') == 'your_claude_api_key_here':
        print("ERROR: Please set your CLAUDE_API_KEY in the env/.env file")
        print("Current value:", os.getenv('CLAUDE_API_KEY', 'Not set'))
        return
    
    try:
        # Path to the CSV file
        csv_file_path = CSV_FILE_PATH
        
        # Check if CSV file exists
        if not Path(csv_file_path).exists():
            print(f"ERROR: CSV file not found at {csv_file_path}")
            return
        
        print(f"Starting evaluation process...")
        print(f"CSV file: {csv_file_path}")
        print(f"Sample size: {SAMPLE_SIZE} questions")
        print("-" * 60)
        
        # Create evaluator and process questions
        evaluator = DifficultyEvaluator(csv_file_path)
        summary = evaluator.process_questions(sample_size=SAMPLE_SIZE)
        
        # Print results
        print("\n" + "="*50)
        print("DIFFICULTY EVALUATION COMPLETE")
        print("="*50)
        print(f"Total questions processed: {summary['total_processed']}")
        print(f"Successfully evaluated: {summary['successfully_evaluated']}")
        print(f"Failed evaluations: {summary['failed_evaluations']}")
        print(f"Saved to database: {summary['saved_to_database']}")
        
        # Get detailed summary
        detailed_summary = evaluator.get_processing_summary()
        print(f"\nDifficulty distribution:")
        for level, count in detailed_summary['difficulty_distribution'].items():
            print(f"  Level {level}: {count} questions")
        
        if detailed_summary['failed_questions']:
            print(f"\nFailed questions (first 5):")
            for i, failed in enumerate(detailed_summary['failed_questions'][:5], 1):
                print(f"  {i}. Error: {failed['error']}")
                print(f"     Question ID: {failed['question']['question_id']}")
                print(f"     Instruction: {failed['question']['instruction'][:100]}...")
        
        print("\n" + "="*50)
        print("Process completed successfully!")
        print("Check your PostgreSQL database for the results.")
        print("="*50)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
