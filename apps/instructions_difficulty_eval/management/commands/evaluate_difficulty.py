from django.core.management.base import BaseCommand, CommandError
from apps.instructions_difficulty_eval.difficulty_evaluator import DifficultyEvaluator
import logging


class Command(BaseCommand):
    help = 'Evaluate difficulty of Python programming questions using Claude API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sample-size',
            type=int,
            default=500,
            help='Number of questions to sample and evaluate (default: 500)'
        )
        parser.add_argument(
            '--csv-path',
            type=str,
            default='data/Python Programming Questions Dataset.csv',
            help='Path to the CSV file containing questions'
        )

    def handle(self, *args, **options):
        # Django logging configuration is already set up via settings.py
        # No need for additional basicConfig as it would override Django's logging

        sample_size = options['sample_size']
        csv_path = options['csv_path']

        self.stdout.write(
            self.style.SUCCESS(f'Starting difficulty evaluation for {sample_size} questions...')
        )

        try:
            # Create evaluator and process questions
            evaluator = DifficultyEvaluator(csv_path)
            summary = evaluator.process_questions(sample_size=sample_size)

            # Print results
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS('DIFFICULTY EVALUATION COMPLETE'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(f'Total questions processed: {summary["total_processed"]}')
            self.stdout.write(f'Successfully evaluated: {summary["successfully_evaluated"]}')
            self.stdout.write(f'Failed evaluations: {summary["failed_evaluations"]}')
            self.stdout.write(f'Saved to database: {summary["saved_to_database"]}')

            # Get detailed summary
            detailed_summary = evaluator.get_processing_summary()
            self.stdout.write('\nDifficulty distribution:')
            for level, count in detailed_summary['difficulty_distribution'].items():
                self.stdout.write(f'  Level {level}: {count} questions')

            if detailed_summary['failed_questions']:
                self.stdout.write(self.style.WARNING('\nFailed questions (first 5):'))
                for i, failed in enumerate(detailed_summary['failed_questions'][:5], 1):
                    self.stdout.write(f'  {i}. Error: {failed["error"]}')
                    self.stdout.write(f'     Instruction: {failed["question"]["instruction"][:100]}...')

            self.stdout.write(
                self.style.SUCCESS(f'\nSuccessfully completed evaluation!')
            )

        except Exception as e:
            raise CommandError(f'Error during evaluation: {e}') 