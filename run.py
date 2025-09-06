import sys
import os
from pathlib import Path
import streamlit as st

# Add the project root to the Python path
project_root = str(Path(__file__).parent.absolute())
if project_root not in sys.path:
    sys.path.append(project_root)

# Set page config - this must be the first Streamlit command
st.set_page_config(
    page_title="Confluence AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import app components after setting page config
from app.main import show_landing_page, show_sidebar

def main():
    # Initialize session state if not already done
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    
    # Show the sidebar with navigation
    show_sidebar()
    
    # Render the appropriate page
    if st.session_state.page == "home":
        show_landing_page()
    else:
        try:
            from app.pages.dashboard import show_dashboard
            show_dashboard()
        except Exception as e:
            st.error(f"Error loading dashboard: {str(e)}")
            st.info("Please make sure you have set up the required environment variables and installed all dependencies.")
            if st.button("Go to Home"):
                st.session_state.page = "home"
                st.rerun()

if __name__ == "__main__":
    main()
