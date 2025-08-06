import pandas as pd
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Class for processing the Python programming questions dataset.
    """
    
    def __init__(self, csv_file_path: str):
        """
        Initialize the data processor with CSV file path.
        
        Args:
            csv_file_path (str): Path to the CSV file containing questions
        """
        self.csv_file_path = Path(csv_file_path)
        self.data = None
        self.sample_data = None
    
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            Exception: If there's an error loading the data
        """
        try:
            if not self.csv_file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
            
            self.data = pd.read_csv(self.csv_file_path)
            logger.info(f"Loaded {len(self.data)} questions from {self.csv_file_path}")
            logger.info(f"Data shape: {self.data.shape}")
            logger.info(f"Columns: {list(self.data.columns)}")
            
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data from {self.csv_file_path}: {e}")
            raise
    
    def sample_questions(self, n: int = 500, random_state: int = 42) -> pd.DataFrame:
        """
        Sample n questions from the dataset.
        
        Args:
            n (int): Number of questions to sample
            random_state (int): Random state for reproducibility
            
        Returns:
            pd.DataFrame: Sampled questions
        """
        try:
            if self.data is None:
                self.load_data()
            
            # Ensure we don't sample more than available data
            sample_size = min(n, len(self.data))
            
            self.sample_data = self.data.sample(n=sample_size, random_state=random_state)
            logger.info(f"Sampled {len(self.sample_data)} questions")
            
            return self.sample_data
            
        except Exception as e:
            logger.error(f"Error sampling questions: {e}")
            raise
    
    def get_questions_list(self) -> List[Dict[str, Any]]:
        """
        Convert sampled questions to a list of dictionaries.
        
        Returns:
            List[Dict[str, Any]]: List of question dictionaries
        """
        try:
            if self.sample_data is None:
                raise ValueError("No sampled data available. Call sample_questions() first.")
            
            questions_list = []
            for _, row in self.sample_data.iterrows():
                question_dict = {
                    'instruction': str(row.get('Instruction', '')).strip(),
                    'input': str(row.get('Input', '')).strip() if pd.notna(row.get('Input')) else '',
                    'output': str(row.get('Output', '')).strip() if pd.notna(row.get('Output')) else ''
                }
                questions_list.append(question_dict)
            
            logger.info(f"Converted {len(questions_list)} questions to dictionary format")
            return questions_list
            
        except Exception as e:
            logger.error(f"Error converting questions to list: {e}")
            raise
    
    def validate_question_data(self, question: Dict[str, Any]) -> bool:
        """
        Validate that a question has the required fields.
        
        Args:
            question (Dict[str, Any]): Question dictionary
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['instruction', 'input', 'output']
        
        for field in required_fields:
            if field not in question:
                logger.warning(f"Missing field '{field}' in question")
                return False
        
        # Check if instruction is not empty
        if not question['instruction'] or question['instruction'].strip() == '':
            logger.warning("Empty instruction found")
            return False
        
        return True 