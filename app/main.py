import streamlit as st
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = str(Path(__file__).parent.absolute())
if app_dir not in sys.path:
    sys.path.append(app_dir)

# Load environment variables
load_dotenv()

# Initialize session state variables in a single place
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.page = "home"
        st.session_state.page_id = ""
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.confluence_service = None
        st.session_state.openai_service = None
        st.session_state.page_content = None

# Initialize session state
init_session_state()

# Custom CSS - only include this once
custom_css = """
<style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        background-color: #0052CC;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #0065FF;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
    }
    .header {
        background: linear-gradient(90deg, #0052CC 0%, #0065FF 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        height: 100%;
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #0052CC;
    }
    /* Hide the default Streamlit header and footer */
    header[data-testid="stHeader"] {
        display: none;
    }
    footer[data-testid="stFooter"] {
        display: none;
    }
    /* Add some padding to the main content */
    .block-container {
        padding-top: 2rem;
    }
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

def show_sidebar():
    """Display the sidebar with navigation and configuration options."""
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Confluence_Logo.svg/1200px-Confluence_Logo.svg.png", 
                width=200)
        st.title("Confluence AI")
        
        # Navigation
        st.markdown("### Navigation")
        
        # Home button
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()
            
        # Dashboard button
        if st.button("📊 Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        
        st.markdown("---")
        
        # Configuration section
        st.markdown("### Configuration")
        
        # Only show these in dashboard
        if st.session_state.page == "dashboard":
            page_id = st.text_input(
                "Confluence Page ID", 
                value=st.session_state.get('page_id', ''),
                help="Enter the Confluence page ID you want to analyze"
            )
            
            if st.button("Load Page", type="primary"):
                if page_id:
                    st.session_state.page_id = page_id
                    # Clear previous page content when loading a new page
                    if 'page_content' in st.session_state:
                        del st.session_state.page_content
                    st.success(f"Page ID set to: {page_id}")
                    st.rerun()
                else:
                    st.error("Please enter a valid page ID")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This is a POC for an AI-powered Confluence assistant that helps you find and understand information across your Confluence spaces.")

def show_landing_page():
    """Display the landing page content."""
    st.markdown("""
    <div class="header">
        <h1 style='color: white;'>Confluence AI Assistant</h1>
        <p style='font-size: 1.2rem;'>Your intelligent companion for Confluence knowledge management</p>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    st.subheader("🚀 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <h3>Smart Search</h3>
            <p>Find answers instantly across all your Confluence spaces with AI-powered search.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered</h3>
            <p>Get accurate, contextual answers using advanced natural language processing.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Lightning Fast</h3>
            <p>Quickly access the information you need without digging through pages.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Get Started Section
    st.markdown("---")
    st.subheader("🚀 Get Started")
    
    st.write("""
    Ready to supercharge your Confluence experience? Get started now by:
    1. Entering your Confluence page ID in the sidebar
    2. Clicking 'Load Page'
    3. Asking questions about the content
    """)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Confluence_Logo.svg/1200px-Confluence_Logo.svg.png", 
             width=200)
    st.title("Confluence AI")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["🏠 Home", "📊 Dashboard"],
        index=0 if st.session_state.page == "home" else 1
    )
    
    # Update page state based on navigation
    if page == "📊 Dashboard":
        st.session_state.page = "dashboard"
    else:
        st.session_state.page = "home"
    
    st.markdown("---")
    st.markdown("### Configuration")
    
    # Only show these in dashboard
    if st.session_state.page == "dashboard":
        page_id = st.text_input("Confluence Page ID", 
                              value=os.getenv("DEFAULT_PAGE_ID", ""),
                              help="Enter the Confluence page ID you want to analyze")
        
        if st.button("Load Page", type="primary"):
            if page_id:
                st.session_state.page_id = page_id
                st.success(f"Page ID set to: {page_id}")
            else:
                st.error("Please enter a valid page ID")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This is a POC for an AI-powered Confluence assistant that helps you find and understand information across your Confluence spaces.")

# Main content
if st.session_state.page == "home":
    show_landing_page()
else:
    # Import and show dashboard
    try:
        from app.pages.dashboard import show_dashboard
        show_dashboard()
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please make sure you have set up the required environment variables and installed all dependencies.")
        if st.button("Go to Home", type="primary"):
            st.session_state.page = "home"
            st.rerun()
