#!/usr/bin/env python3
"""
Sample Data Script

This script demonstrates how to load and sample data from the Python Programming Questions Dataset.
It creates a df_sample dataframe with SAMPLE_SIZE sampled questions.

Usage:
    python test_sample_data.py
"""
import sys
import pandas as pd
import logging
from pathlib import Path

#CSV_FILE_PATH = "data/Python Programming Questions Dataset.csv"
#SAMPLE_SIZE = 10

CSV_FILE_PATH = "data/sample_questions.csv"
SAMPLE_SIZE = 5

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from apps.instructions_difficulty_eval.data_processor import DataProcessor

# Configure Django environment for logging
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_interview_preparation_platform.settings')
django.setup()

# Django logging configuration is already set up via settings.py

logger = logging.getLogger(__name__)


def create_sample_dataframe(csv_path: str = CSV_FILE_PATH, 
                          sample_size: int = SAMPLE_SIZE) -> pd.DataFrame:
    """
    Create a sample dataframe from the Python Programming Questions Dataset.
    
    Args:
        csv_path (str): Path to the CSV file
        sample_size (int): Number of questions to sample
        
    Returns:
        pd.DataFrame: Sampled dataframe (df_sample)
    """
    try:
        # Initialize data processor
        processor = DataProcessor(csv_path)
        
        # Load and sample data
        df_sample = processor.sample_questions(n=sample_size, random_state=42)
        
        logger.info(f"Created df_sample with {len(df_sample)} questions")
        logger.info(f"Columns: {list(df_sample.columns)}")
        logger.info(f"Sample shape: {df_sample.shape}")
        
        return df_sample
        
    except Exception as e:
        logger.error(f"Error creating sample dataframe: {e}")
        raise


def display_sample_info(df_sample: pd.DataFrame) -> None:
    """
    Display information about the sampled dataframe.
    
    Args:
        df_sample (pd.DataFrame): The sampled dataframe
    """
    print("="*60)
    print("SAMPLE DATAFRAME INFORMATION")
    print("="*60)
    print(f"Shape: {df_sample.shape}")
    print(f"Columns: {list(df_sample.columns)}")
    print(f"Memory usage: {df_sample.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    print("\nFirst 3 sample instructions:")
    print("-" * 40)
    for i, instruction in enumerate(df_sample['Instruction'].head(3), 1):
        print(f"{i}. {instruction[:100]}...")
    
    print("\nData types:")
    print("-" * 20)
    print(df_sample.dtypes)
    
    print("\nMissing values:")
    print("-" * 20)
    print(df_sample.isnull().sum())


def main():
    """
    Main function to demonstrate data sampling.
    """
    try:
        # Create sample dataframe
        df_sample = create_sample_dataframe()
        
        # Display information
        display_sample_info(df_sample)
        
        # Save sample to CSV for inspection
        output_path = "data/sample_questions_output.csv"
        df_sample.to_csv(output_path, index=False)
        print(f"\nSample saved to: {output_path}")
        
        print("\n" + "="*60)
        print("Sample dataframe created successfully!")
        print("You can now use 'df_sample' for further processing.")
        print("="*60)
        
        return df_sample
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    df_sample = main() 