import os
import sys
import django
import logging
from typing import List, Dict, Any
from pathlib import Path
from tqdm import tqdm

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from apps.instructions_difficulty_eval.difficulty_service import DifficultyEvaluationService
from apps.instructions_difficulty_eval.data_processor import DataProcessor

logger = logging.getLogger(__name__)


class DifficultyEvaluator:
    """
    Main class that orchestrates the difficulty evaluation process.
    """
    
    def __init__(self, csv_file_path: str):
        """
        Initialize the difficulty evaluator.
        
        Args:
            csv_file_path (str): Path to the CSV file containing questions
        """
        self.csv_file_path = csv_file_path
        self.data_processor = DataProcessor(csv_file_path)
        self.difficulty_service = DifficultyEvaluationService()
        self.processed_questions = []
        self.failed_questions = []
        self.saved_count = 0
    
    def process_questions(self, sample_size: int = 500) -> Dict[str, int]:
        """
        Process questions by evaluating difficulty and saving to database.
        
        Args:
            sample_size (int): Number of questions to sample and process
            
        Returns:
            Dict[str, int]: Summary of processing results
        """
        try:
            logger.info(f"Starting difficulty evaluation for {sample_size} questions")
            
            # Load and sample data
            self.data_processor.sample_questions(n=sample_size)
            questions_list = self.data_processor.get_questions_list()
            
            logger.info(f"Processing {len(questions_list)} questions")
            
            # Process each question
            for i, question in enumerate(tqdm(questions_list, desc="Processing questions"), 1):
                try:
                    self._process_single_question(question, i, len(questions_list))
                except Exception as e:
                    logger.error(f"Error processing question {i}: {e}")
                    self.failed_questions.append({
                        'question': question,
                        'error': str(e)
                    })
            
            # Return summary
            summary = {
                'total_processed': len(questions_list),
                'successfully_evaluated': len(self.processed_questions),
                'failed_evaluations': len(self.failed_questions),
                'saved_to_database': self.saved_count
            }
            
            logger.info(f"Processing complete: {summary}")
            return summary
            
        except Exception as e:
            logger.error(f"Error in process_questions: {e}")
            raise
    
    def _process_single_question(self, question: Dict[str, Any], current: int, total: int) -> None:
        """
        Process a single question by evaluating its difficulty and saving to database.
        
        Args:
            question (Dict[str, Any]): Question data
            current (int): Current question number
            total (int): Total number of questions
        """
        try:
            # Validate question data
            if not self.data_processor.validate_question_data(question):
                logger.warning(f"Question {current} failed validation, skipping")
                return
            
            instruction = question['instruction']
            logger.info(f"Processing question {current}/{total}: {instruction[:50]}...")

            input = question['input']
            output = question['output']
            
            # Evaluate explanation and numeric difficulty level using Claude API
            explanation_text, difficulty_level = self.difficulty_service.evaluate_instruction_difficulty(instruction, input, output)
            
            question['question_id'] = current
            if difficulty_level is not None:
                # Add explanation and difficulty level to question data
                question['difficulty_explanation'] = explanation_text
                question['difficulty_level'] = difficulty_level

                self.processed_questions.append(question)

                logger.info(f"Question {current} evaluated with difficulty level: {difficulty_level}")

                is_saved = self._save_to_database(question)
                if not is_saved:
                    logger.error(f"Failed to save question {current} to database")
                    self.failed_questions.append({
                        'question': question,
                        'error': 'Failed to save question to database'
                    })
            else:
                logger.warning(f"Failed to evaluate difficulty for question {current}")
                self.failed_questions.append({
                    'question': question,
                    'error': 'Failed to get difficulty level from Claude API'
                })
                
        except Exception as e:
            logger.error(f"Error processing single question {current}: {e}")
            raise
    
    def _save_to_database(self, question: Dict[str, Any]) -> bool:
        """
        Save processed question to the database and update the saved_count.
        
        Args:
            question (Dict[str, Any]): Question data

        Returns:
            bool: True if question was saved to database, False otherwise
        """
        try:
            logger.info(f"Saving question to database")
            
            # Create and save the model instance
            python_question = PythonProgrammingQuestion(
                instruction=question['instruction'],
                input=question['input'],
                output=question['output'],
                difficulty_explanation=question['difficulty_explanation'],
                difficulty_level=question['difficulty_level']
            )
            python_question.save()
            self.saved_count += 1
            return True
            
        except Exception as e:
            logger.error(f"Error saving question to database: {e}")
            logger.error(f"Question data: {question}")
            return False
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get a detailed summary of the processing results.
        
        Returns:
            Dict[str, Any]: Detailed processing summary
        """
        return {
            'processed_questions_count': len(self.processed_questions),
            'failed_questions_count': len(self.failed_questions),
            'failed_questions': self.failed_questions,
            'difficulty_distribution': self._get_difficulty_distribution()
        }
    
    def _get_difficulty_distribution(self) -> Dict[int, int]:
        """
        Get the distribution of difficulty levels in processed questions.
        
        Returns:
            Dict[int, int]: Distribution of difficulty levels
        """
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for question in self.processed_questions:
            difficulty = question.get('difficulty_level')
            if difficulty in distribution:
                distribution[difficulty] += 1
        
        return distribution


def main():
    """
    Main function to run the difficulty evaluation process.
    """
    # Django logging configuration is already set up via settings.py
    # No need for additional basicConfig as it would override Django's logging
    
    try:
        # Path to the CSV file
        csv_file_path = "data/Python Programming Questions Dataset.csv"
        
        # Create evaluator and process questions
        evaluator = DifficultyEvaluator(csv_file_path)
        summary = evaluator.process_questions(sample_size=500)
        
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
            print(f"\nFailed questions:")
            for i, failed in enumerate(detailed_summary['failed_questions'][:5], 1):
                print(f"  {i}. Error: {failed['error']}")
                print(f"     Instruction: {failed['question']['instruction'][:100]}...")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 