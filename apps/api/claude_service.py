import os
import logging
from typing import Dict, List, Any
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeService:
    """
    Generic service class for interacting with Claude API.
    This can be used across different Django apps for various AI tasks.
    """
    
    def __init__(self):
        """
        Initialize Claude API client.
        """
        self.api_key = os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY environment variable is required")
        
        self.client = Anthropic(api_key=self.api_key)
        # Using Claude 4 Sonnet, which is the latest available model
        self.model = "claude-sonnet-4-20250514"
    
    def send_message(
        self, 
        prompt: str, 
        max_tokens: int = 21333,
        temperature: float = 0.1,
        system_message: str = None,
        thinking_mode: bool = True
    ) -> str:
        """
        Send a message to Claude and get a response.
        
        Args:
            prompt: The user prompt to send
            max_tokens: Maximum tokens in response (includes both thinking + answer when thinking_mode=True)
                       Default: 21,333 (maximum without streaming requirement)
                       Automatically increased to minimum 1124 when thinking_mode=True
            temperature: Temperature for response generation (0-1) - ignored when thinking_mode=True (uses 1.0)
            system_message: Optional system message
            thinking_mode: If True, use Claude Advanced Thinking Mode with budget tokens
            
        Returns:
            str: Claude's response text
        """
        try:
            messages = []
            
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages
            }
            
            # Add thinking mode parameters if enabled
            if thinking_mode:
                # Ensure max_tokens is sufficient for thinking mode (minimum 1024 + buffer)
                min_required_tokens = 1024 + 100  # 1024 minimum budget + 100 buffer
                if max_tokens < min_required_tokens:
                    max_tokens = min_required_tokens
                    api_params["max_tokens"] = max_tokens
                
                # Use maximum budget tokens (Claude 4 summarizes thinking output)
                # Only need small buffer since thinking is summarized, not full output
                budget_tokens = max_tokens - 100  # Minimal buffer as thinking is summarized
                budget_tokens = max(budget_tokens, 1024)  # Ensure minimum 1024 as required
                
                api_params["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": budget_tokens
                }
                # Temperature must be 1 when thinking is enabled (per API docs)
                api_params["temperature"] = 1.0
            else:
                # Only set temperature when thinking is disabled
                api_params["temperature"] = temperature
            
            response = self.client.messages.create(**api_params)
            
            # Find the text content block (thinking blocks come first, then text blocks)
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            
            # Fallback if no text block found
            return ""
            
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            raise
    
    def send_structured_message(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 21333,
        temperature: float = 0.1,
        thinking_mode: bool = True
    ) -> str:
        """
        Send structured messages to Claude.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum tokens in response (includes both thinking + answer when thinking_mode=True)
                       Default: 21,333 (maximum without streaming requirement)
                       Automatically increased to minimum 1124 when thinking_mode=True
            temperature: Temperature for response generation (0-1) - ignored when thinking_mode=True (uses 1.0)
            thinking_mode: If True, use Claude Advanced Thinking Mode with budget tokens
            
        Returns:
            str: Claude's response text
        """
        try:
            # Prepare API call parameters
            api_params = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": messages
            }
            
            # Add thinking mode parameters if enabled
            if thinking_mode:
                # Ensure max_tokens is sufficient for thinking mode (minimum 1024 + buffer)
                min_required_tokens = 1024 + 100  # 1024 minimum budget + 100 buffer
                if max_tokens < min_required_tokens:
                    max_tokens = min_required_tokens
                    api_params["max_tokens"] = max_tokens
                
                # Use maximum budget tokens (Claude 4 summarizes thinking output)
                # Only need small buffer since thinking is summarized, not full output
                budget_tokens = max_tokens - 100  # Minimal buffer as thinking is summarized
                budget_tokens = max(budget_tokens, 1024)  # Ensure minimum 1024 as required
                
                api_params["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": budget_tokens
                }
                # Temperature must be 1 when thinking is enabled (per API docs)
                api_params["temperature"] = 1.0
            else:
                # Only set temperature when thinking is disabled
                api_params["temperature"] = temperature
            
            response = self.client.messages.create(**api_params)
            
            # Find the text content block (thinking blocks come first, then text blocks)
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            
            # Fallback if no text block found
            return ""
            
        except Exception as e:
            logger.error(f"Error calling Claude API with structured messages: {e}")
            raise 