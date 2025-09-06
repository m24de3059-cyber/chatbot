import os
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add the app directory to the Python path
app_dir = str(Path(__file__).parent.parent.absolute())
if app_dir not in sys.path:
    sys.path.append(app_dir)

# Import third-party libraries
try:
    from atlassian import Confluence
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install the required packages with: pip install atlassian-python-api beautifulsoup4")
    sys.exit(1)

logger = logging.getLogger(__name__)

class ConfluenceService:
    """Service for interacting with Confluence API."""
    
    def __init__(self):
        """
        Initialize the Confluence client with environment variables.
        
        Raises:
            ValueError: If required environment variables are not set
            Exception: If client initialization fails
        """
        self.url = os.getenv("CONFLUENCE_URL")
        self.email = os.getenv("CONFLUENCE_EMAIL")
        self.api_token = os.getenv("CONFLUENCE_API_TOKEN")
        
        # Validate required environment variables
        if not all([self.url, self.email, self.api_token]):
            error_msg = (
                "Missing required environment variables. "
                "Please set CONFLUENCE_URL, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        self.client = self._get_client()
    
    def _get_client(self) -> Confluence:
        """
        Create and return a Confluence client instance.
        
        Returns:
            Confluence: An authenticated Confluence client instance
            
        Raises:
            Exception: If client initialization fails
        """
        try:
            logger.info(f"Initializing Confluence client for {self.email} at {self.url}")
            client = Confluence(
                url=self.url,
                username=self.email,
                password=self.api_token,
                cloud=True,
                verify_ssl=True  # Enable SSL verification for security
            )
            
            # Test the connection
            client.get_server_info()
            logger.info("Successfully connected to Confluence")
            return client
            
        except Exception as e:
            error_msg = f"Failed to initialize Confluence client: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e
    
    def get_page(self, page_id: str) -> Optional[Dict]:
        """
        Get a Confluence page by ID.
        
        Args:
            page_id: The ID of the page to retrieve
            
        Returns:
            Dict containing page data or None if not found
        """
        try:
            page = self.client.get_page_by_id(
                page_id=page_id,
                expand='body.storage,version,ancestors,descendants.page,metadata.labels'
            )
            
            # Extract relevant data
            return {
                'id': page['id'],
                'title': page['title'],
                'url': f"{self.url.rstrip('/')}/wiki{page['_links']['webui']}",
                'content': self._clean_html(page['body']['storage']['value']),
                'version': page['version']['number'],
                'last_updated': page['version']['when'],
                'created': page['history']['createdDate'],
                'space': page.get('space', {}).get('name', 'Unknown'),
                'labels': [label['name'] for label in page.get('metadata', {}).get('labels', {}).get('results', [])],
                'ancestors': [ancestor['title'] for ancestor in page.get('ancestors', [])],
                'child_pages': [child['title'] for child in page.get('descendants', {}).get('page', {}).get('results', [])]
            }
            
        except Exception as e:
            logger.error(f"Error fetching page {page_id}: {str(e)}")
            return None
    
    def _clean_html(self, html_content: str) -> str:
        """
        Clean HTML content and extract text.
        
        Args:
            html_content: Raw HTML content from Confluence
            
        Returns:
            Cleaned text content
        """
        if not html_content:
            return ""
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(["script", "style", "noscript"]):
            element.decompose()
            
        # Get text and clean up
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up multiple whitespace and newlines
        return ' '.join(text.split())
    
    def search_pages(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for pages in Confluence.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching pages with basic info
        """
        try:
            results = self.client.cql(
                f'siteSearch ~ "{query}"',
                limit=limit,
                expand='content.version,content.space'
            )
            
            return [
                {
                    'id': result['content']['id'],
                    'title': result['content']['title'],
                    'space': result['content']['space']['name'],
                    'last_updated': result['content']['version']['when']
                }
                for result in results.get('results', [])
                if result.get('content')
            ]
            
        except Exception as e:
            logger.error(f"Error searching pages: {str(e)}")
            return []

    def get_page_content_chunked(self, page_id: str, chunk_size: int = 2000) -> List[Dict]:
        """
        Get page content split into chunks for processing.
        
        Args:
            page_id: The ID of the page
            chunk_size: Maximum size of each chunk in characters
            
        Returns:
            List of chunks with metadata
        """
        page = self.get_page(page_id)
        if not page or not page.get('content'):
            return []
            
        content = page['content']
        chunks = []
        
        # Simple chunking by character count
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            chunks.append({
                'text': chunk,
                'chunk_id': f"{page_id}_{len(chunks)}",
                'page_id': page_id,
                'page_title': page['title']
            })
            
        return chunks
