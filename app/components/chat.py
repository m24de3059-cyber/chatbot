import streamlit as st
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = str(Path(__file__).parent.parent.absolute())
if app_dir not in sys.path:
    sys.path.append(app_dir)

class ChatManager:
    """Manages chat interactions and state."""
    
    @staticmethod
    def initialize_session_state() -> None:
        """Initialize chat-related session state variables if they don't exist."""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
    
    @staticmethod
    def display_chat_messages() -> None:
        """Display chat messages from the session state."""
        if not hasattr(st.session_state, 'messages') or not st.session_state.messages:
            return
            
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    @staticmethod
    def add_user_message(content: str) -> None:
        """Add a user message to the chat."""
        if not hasattr(st.session_state, 'messages'):
            st.session_state.messages = []
        if not hasattr(st.session_state, 'chat_history'):
            st.session_state.chat_history = []
            
        st.session_state.messages.append({"role": "user", "content": content})
        st.session_state.chat_history.append({
            "role": "user",
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    def add_assistant_message(content: str) -> None:
        """Add an assistant message to the chat."""
        if not hasattr(st.session_state, 'messages'):
            st.session_state.messages = []
        if not hasattr(st.session_state, 'chat_history'):
            st.session_state.chat_history = []
            
        st.session_state.messages.append({"role": "assistant", "content": content})
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    def get_chat_history() -> List[Dict]:
        """Get the chat history."""
        return st.session_state.get('chat_history', [])
    
    @staticmethod
    def clear_chat() -> None:
        """Clear the chat history while keeping the context."""
        if hasattr(st.session_state, 'messages'):
            st.session_state.messages = []
        
        # Keep the chat history for logging
        if not hasattr(st.session_state, 'chat_history'):
            st.session_state.chat_history = []

def show_chat_interface() -> None:
    """Display the chat interface."""
    # Initialize chat state
    ChatManager.initialize_session_state()
    
    # Display chat messages
    ChatManager.display_chat_messages()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about this page..."):
        # Add user message to chat
        ChatManager.add_user_message(prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner('Thinking...'):
                try:
                    # Get the page content from session state
                    page_content = st.session_state.get('page_content', {})
                    
                    # Generate answer using OpenAI service
                    if 'openai_service' in st.session_state and page_content:
                        response = st.session_state.openai_service.generate_answer(
                            context=page_content.get('content', ''),
                            question=prompt
                        )
                    else:
                        response = "I'm sorry, I couldn't process your request. The page content is not available."
                    
                    # Display the response
                    st.markdown(response)
                    
                    # Add assistant response to chat
                    ChatManager.add_assistant_message(response)
                except Exception as e:
                    error_msg = f"An error occurred while processing your request: {str(e)}"
                    st.error(error_msg)
                    ChatManager.add_assistant_message(error_msg)
        
        # Rerun to update the chat
        st.rerun()
    
    # Add a button to clear chat
    if st.button("Clear Chat"):
        ChatManager.clear_chat()
        st.rerun()

def export_chat_history() -> Tuple[Optional[str], Optional[str]]:
    """
    Export chat history to a JSON file.
    
    Returns:
        Tuple containing (json_string, filename) or (None, None) if no history
    """
    if hasattr(st.session_state, 'chat_history') and st.session_state.chat_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        return json.dumps(st.session_state.chat_history, indent=2), filename
    
    return None, None
