import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.resolve()

# Confluence Configuration
CONFLUENCE_CONFIG = {
    'URL': os.getenv('CONFLUENCE_URL', 'https://your-domain.atlassian.net'),
    'EMAIL': os.getenv('CONFLUENCE_EMAIL', 'your-email@example.com'),
    'API_TOKEN': os.getenv('CONFLUENCE_API_TOKEN', 'your-api-token'),
    'DEFAULT_PAGE_ID': os.getenv('DEFAULT_PAGE_ID'),  # Optional: Set a default page ID
}

# OpenAI Configuration
OPENAI_CONFIG = {
    'API_KEY': os.getenv('OPENAI_API_KEY', ''),
    'MODEL': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
    'TEMPERATURE': float(os.getenv('OPENAI_TEMPERATURE', '0.3')),
    'MAX_TOKENS': int(os.getenv('OPENAI_MAX_TOKENS', '1000')),
}

# Application Settings
APP_CONFIG = {
    'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
    'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
    'CACHE_DIR': os.path.join(BASE_DIR, '.cache'),
    'OUTPUT_DIR': os.path.join(BASE_DIR, 'output'),
    'UPLOAD_FOLDER': os.path.join(BASE_DIR, 'uploads'),
}

# UI Settings
UI_CONFIG = {
    'PAGE_TITLE': 'Confluence AI Assistant',
    'PAGE_ICON': '🤖',
    'LAYOUT': 'wide',
    'INITIAL_SIDEBAR_STATE': 'expanded',
}

def ensure_directories():
    """Ensure all required directories exist."""
    os.makedirs(APP_CONFIG['CACHE_DIR'], exist_ok=True)
    os.makedirs(APP_CONFIG['OUTPUT_DIR'], exist_ok=True)
    os.makedirs(APP_CONFIG['UPLOAD_FOLDER'], exist_ok=True)

# Initialize directories
ensure_directories()

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': APP_CONFIG['LOG_LEVEL'],
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'level': 'DEBUG',
            'filename': os.path.join(APP_CONFIG['OUTPUT_DIR'], 'app.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'confluence': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'openai': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'streamlit': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False
        },
        'urllib3': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}
