import logging
from typing import Tuple, Optional
from langchain.prompts import PromptTemplate
from apps.api import ClaudeService

logger = logging.getLogger(__name__)


class DifficultyEvaluationService:
    """
    Service for evaluating Python programming question difficulty using Claude API.
    """
    
    def __init__(self):
        """Initialize the service with Claude API client."""
        self.claude_service = ClaudeService()
    
    def evaluate_instruction_difficulty(
        self, 
        instruction: str, 
        input: str, 
        output: str
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Evaluate the explanation and difficulty level of a programming instruction.
        
        Args:
            instruction: The programming instruction to evaluate
            input: Input example for the question
            output: Expected output for the question
            
        Returns:
            tuple[str, int]: Explanation text and numeric difficulty level (1-5), 
                           or (None, None) if evaluation fails
        """
        try:
            prompt = self._create_difficulty_evaluation_prompt(instruction, input, output)
            
            response_text = self.claude_service.send_message(
                prompt=prompt,
                temperature=0.1
            )
            
            # Parse the response
            explanation_text, difficulty_level = self._parse_difficulty_response(response_text)
            return explanation_text, difficulty_level
            
        except Exception as e:
            logger.error(f"Error evaluating instruction difficulty: {e}")
            logger.error(f"Instruction: {instruction[:100]}...")
            return None, None
    
    def _create_difficulty_evaluation_prompt(self, instruction: str, input: str, output: str) -> str:
        """
        Create a prompt for Claude to evaluate instruction difficulty.
        
        Args:
            instruction: The programming instruction
            input: Input example
            output: Expected output
            
        Returns:
            str: Formatted prompt for Claude API
        """
        prompt_template = PromptTemplate(
            input_variables=["instruction", "input", "output"],
            template="""Please help me with the task of ranking the difficulty level of a Python programming question (instruction),   
                given the input and output.

                The instruction, input and output are given at the end of this prompt.

                The instruction should be assigned a numeric difficulty level (1, 2, 3, 4, or 5). (1 - easiest, 5 - hardest). 

                Here are the difficulty level definitions:
                **1 = Very Easy (Beginner - Basic Python Syntax)**
                - Simple arithmetic operations and basic calculations
                - Basic print statements and variable assignments
                - Simple list/string operations without complex logic
                - Basic loops and conditionals with straightforward logic
                - Examples: "Calculate sum of two numbers", "Print numbers 1-10", "Check if number is even"

                **2 = Easy (Fundamental Programming Concepts)**
                - Basic function definitions with simple parameters
                - Elementary list/dictionary manipulation
                - Simple string processing and formatting
                - Basic file operations
                - Straightforward control flow with multiple conditions
                - Examples: "Remove duplicates from list", "Count occurrences in string", "Basic calculator functions"

                **3 = Medium (Intermediate Python Features)**
                - List comprehensions and lambda functions
                - Basic sorting and searching algorithms
                - Simple recursion (Fibonacci, factorial)
                - Basic object-oriented programming (simple classes)
                - Exception handling
                - Working with modules and imports
                - Examples: "Binary search implementation", "Simple class definitions", "Recursive functions"

                **4 = Hard (Advanced Programming Concepts)**
                - Complex data structures (linked lists, trees, stacks)
                - Advanced algorithms (DFS, BFS, dynamic programming)
                - Web scraping and API interactions
                - Database connections and operations
                - Advanced OOP concepts (inheritance, polymorphism)
                - Regular expressions and pattern matching
                - Examples: "Binary tree traversal", "Web scraping with BeautifulSoup", "REST API development"

                **5 = Very Hard (Expert Level - Professional Development)**
                - Machine learning model implementation
                - Asynchronous programming and concurrency
                - Advanced data analysis with NumPy/Pandas
                - Cloud services integration (AWS Lambda)
                - Complex system design and architecture
                - Performance optimization and algorithm complexity
                - Advanced web development frameworks
                - Examples: "ML classifier with scikit-learn", "AWS Lambda functions", "Asynchronous web scraping"

                Please respond with:
                (1) All the text explaning how you decided upon the difficulty level.
                (2) The last character at the very end should be the difficulty level numeric value (1, 2, 3, 4, or 5) alone, 
                without '**' or any other text. 

                Instruction: "{instruction}"
                Input: "{input}"
                Output: "{output}"
                """
        )
        return prompt_template.format(
            instruction=instruction,
            input=input,
            output=output
        )
    
    def _parse_difficulty_response(self, response_text: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Parse the explanation and difficulty level from Claude's response.
        
        Args:
            response_text: Claude's response text
            
        Returns:
            tuple[str, int]: Parsed explanation text and numeric difficulty level,
                           or (None, None) if parsing fails
        """
        try:
            difficulty_str = response_text.strip()

            # Extract explanation text from response
            explanation_text = difficulty_str[0:-1]

            # Extract numeric value from response
            numeric_difficulty_str = difficulty_str[-1]
            if numeric_difficulty_str.isdigit():
                numeric_difficulty = int(numeric_difficulty_str)
                if 1 <= numeric_difficulty <= 5:
                    return explanation_text, numeric_difficulty
                        
            logger.warning(f"Could not parse difficulty from response: {response_text}")
            return None, None
            
        except Exception as e:
            logger.error(f"Error parsing difficulty response: {e}")
            return None, None 