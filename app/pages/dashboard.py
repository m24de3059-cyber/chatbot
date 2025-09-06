import streamlit as st
from datetime import datetime
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
app_dir = str(Path(__file__).parent.parent.absolute())
if app_dir not in sys.path:
    sys.path.append(app_dir)

# Import services and components
try:
    from app.services.confluence_service import ConfluenceService
    from app.services.openai_service import OpenAIService
    from app.components.chat import show_chat_interface
    from app.components.page_info import show_page_info
except ImportError as e:
    st.error(f"Failed to import required modules: {str(e)}")
    st.stop()

def show_dashboard():
    """Display the main dashboard with chat interface and page information."""
    # Don't show title here to avoid duplicate headers
    
    # Initialize services
    try:
        if 'confluence_service' not in st.session_state or st.session_state.confluence_service is None:
            st.session_state.confluence_service = ConfluenceService()
        if 'openai_service' not in st.session_state or st.session_state.openai_service is None:
            st.session_state.openai_service = OpenAIService()
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        st.info("Please check your environment variables and try again.")
        return
    
    # Check if page is loaded
    if 'page_id' not in st.session_state or not st.session_state.page_id:
        st.info("👈 Please enter a Confluence Page ID and click 'Load Page' in the sidebar to get started.")
        return
    
    # Try to load page content if not already loaded
    if 'page_content' not in st.session_state:
        with st.spinner("Loading page content..."):
            try:
                page_content = st.session_state.confluence_service.get_page(st.session_state.page_id)
                if page_content:
                    st.session_state.page_content = page_content
                    st.success(f"Successfully loaded page: {page_content.get('title', 'Untitled')}")
                else:
                    st.error(f"Failed to load page with ID: {st.session_state.page_id}")
                    return
            except Exception as e:
                st.error(f"Error loading page: {str(e)}")
                if st.button("Try Again"):
                    if 'page_content' in st.session_state:
                        del st.session_state.page_content
                    st.rerun()
                return
    
    # Show page title and content
    if 'page_content' in st.session_state and st.session_state.page_content:
        page = st.session_state.page_content
        st.markdown(f"## {page.get('title', 'Untitled')}")
        
        # Two-column layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            show_chat_interface()
        
        with col2:
            show_page_info()
    else:
        st.warning("No page content available. Please load a valid Confluence page.")

# This allows the page to be imported and used by main.py
if __name__ == "__main__":
    show_dashboard()
