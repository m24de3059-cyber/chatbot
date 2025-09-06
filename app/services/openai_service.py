import os
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Add the app directory to the Python path
app_dir = str(Path(__file__).parent.parent.absolute())
if app_dir not in sys.path:
    sys.path.append(app_dir)

# Import third-party libraries
try:
    from openai import OpenAI, OpenAIError
    import tiktoken
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install the required packages with: pip install openai tiktoken")
    sys.exit(1)

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for interacting with OpenAI's API."""
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize the OpenAI client with API key from environment variables.
        
        Args:
            model: The name of the OpenAI model to use (default: "gpt-3.5-turbo")
            
        Raises:
            ValueError: If OPENAI_API_KEY environment variable is not set
            Exception: If client initialization fails
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            error_msg = "OPENAI_API_KEY environment variable not set"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self.model = model
        self.max_tokens = 1000
        self.temperature = 0.3
        
        try:
            logger.info(f"Initializing OpenAI client with model: {self.model}")
            self.client = OpenAI(api_key=self.api_key)
            self.encoding = tiktoken.encoding_for_model(self.model)
            logger.info("Successfully initialized OpenAI client")
        except Exception as e:
            error_msg = f"Failed to initialize OpenAI client: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get embedding vector for the given text.
        
        Args:
            text: Input text to get embedding for
            
        Returns:
            List of floats representing the embedding, or None if failed
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            return None
    
    def generate_answer(self, context: str, question: str, model: str = "gpt-3.5-turbo") -> str:
        """
        Generate an answer to a question based on the provided context.
        
        Args:
            context: The context to base the answer on
            question: The question to answer
            model: The OpenAI model to use
            
        Returns:
            Generated answer as a string
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful assistant that answers questions based on the provided context. 
                    If the answer cannot be found in the context, say \"I couldn't find the answer in the provided content.\"
                    Be concise and to the point in your responses."""
                },
                {
                    "role": "user",
                    "content": f"""Context: {context}
                    \n\nQuestion: {question}"""
                }
            ]
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return "I'm sorry, I encountered an error while processing your request."
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text.
        
        Args:
            text: Input text
            
        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))
    
    def summarize_text(self, text: str, max_tokens: int = 300) -> str:
        """
        Generate a summary of the given text.
        
        Args:
            text: Text to summarize
            max_tokens: Maximum length of the summary in tokens
            
        Returns:
            Generated summary
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes text concisely while preserving key information."
                    },
                    {
                        "role": "user",
                        "content": f"Please summarize the following text concisely:\n\n{text}"
                    }
                ],
                temperature=0.3,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return text[:500] + "..."  # Fallback to first 500 chars if summarization fails
