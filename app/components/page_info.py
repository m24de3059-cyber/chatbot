import streamlit as st
from datetime import datetime
from typing import Any, Dict, Optional
import json
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = str(Path(__file__).parent.parent.absolute())
if app_dir not in sys.path:
    sys.path.append(app_dir)

# Import the chat component for exporting history
from .chat import export_chat_history

def format_datetime(dt_str: str) -> str:
    """
    Format ISO datetime string to a more readable format.
    
    Args:
        dt_str: ISO format datetime string
        
    Returns:
        Formatted datetime string or 'N/A' if invalid
    """
    if not dt_str:
        return "N/A"
        
    try:
        # Handle different datetime formats
        if 'Z' in dt_str:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%B %d, %Y at %H:%M")
    except (ValueError, AttributeError, TypeError) as e:
        return "N/A"

def show_page_info() -> None:
    """Display information about the current Confluence page."""
    if not hasattr(st.session_state, 'page_content') or not st.session_state.page_content:
        st.warning("No page content available. Please load a Confluence page first.")
        return
    
    page = st.session_state.page_content
    
    try:
        st.markdown("### 📄 Page Information")
        
        # Page title with link
        title = page.get('title', 'Untitled')
        url = page.get('url', '#')
        st.markdown(f"#### [{title}]({url})")
        
        # Metadata
        col1, col2 = st.columns(2)
        
        with col1:
            version = page.get('version', '1.0')
            st.metric("Version", f"v{version}")
        
        with col2:
            space = page.get('space', 'N/A')
            st.metric("Space", space)
        
        # Dates
        st.markdown("#### 📅 Dates")
        created = format_datetime(page.get('created'))
        updated = format_datetime(page.get('last_updated'))
        st.markdown(f"- **Created:** {created}")
        st.markdown(f"- **Last Updated:** {updated}")
        
        # Labels
        if page.get('labels'):
            st.markdown("#### 🏷️ Labels")
            labels = ", ".join([f"`{label}`" for label in page.get('labels', []) if label])
            if labels:
                st.markdown(labels)
            else:
                st.caption("No labels")
        
        # Ancestors (breadcrumbs)
        if page.get('ancestors'):
            st.markdown("#### 🗂️ Location")
            try:
                ancestors = [a for a in page.get('ancestors', []) if a]  # Filter out None/empty
                if ancestors and page.get('title'):
                    breadcrumbs = " > ".join(ancestors[::-1] + [page['title']])
                    st.caption(breadcrumbs)
            except Exception:
                pass
        
        # Child pages
        if page.get('child_pages'):
            st.markdown("#### 📂 Child Pages")
            child_pages = [c for c in page.get('child_pages', []) if c]  # Filter out None/empty
            if child_pages:
                for child in child_pages[:5]:  # Show first 5 children
                    st.markdown(f"- {child}")
                if len(child_pages) > 5:
                    st.caption(f"... and {len(child_pages) - 5} more")
            else:
                st.caption("No child pages")
        
        # Export button
        try:
            chat_history, filename = export_chat_history()
            if chat_history and filename:
                st.download_button(
                    label="📥 Export Chat History",
                    data=chat_history,
                    file_name=filename,
                    mime="application/json",
                    key="export_chat_history"
                )
        except Exception as e:
            st.error(f"Failed to prepare chat history export: {str(e)}")
        
        # Debug info (collapsed)
        with st.expander("Debug Info"):
            try:
                st.json(page, expanded=False)
            except Exception as e:
                st.error(f"Failed to display debug info: {str(e)}")
    
    except Exception as e:
        st.error(f"An error occurred while displaying page information: {str(e)}")
        if st.button("Reload Page"):
            st.rerun()
