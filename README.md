# Confluence AI Assistant

A modern, AI-powered chatbot interface for Confluence that allows you to ask questions and get answers from your Confluence pages in a natural, conversational way.

## 🌟 Features

- **AI-Powered Q&A**: Get accurate answers to your questions based on Confluence page content
- **Beautiful UI**: Modern, responsive interface with a clean design
- **Page Information**: View metadata, versions, and relationships of Confluence pages
- **Chat History**: Your conversation history is maintained during the session
- **Export Capabilities**: Export your chat history for future reference
- **Multi-page Support**: Easily switch between different Confluence pages

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Confluence Cloud account with API access
- OpenAI API key

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ANGBOT
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your credentials:
   ```
   # Confluence Settings
   CONFLUENCE_URL=https://your-domain.atlassian.net
   CONFLUENCE_EMAIL=your-email@example.com
   CONFLUENCE_API_TOKEN=your-confluence-api-token
   
   # OpenAI Settings
   OPENAI_API_KEY=your-openai-api-key
   ```

### Getting Your API Keys

1. **Confluence API Token**:
   - Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security)
   - Under "Security", select "Create and manage API tokens"
   - Click "Create API token" and follow the prompts

2. **OpenAI API Key**:
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new secret key

## 🏃‍♂️ Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run app/main.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. In the sidebar:
   - Enter a Confluence Page ID
   - Click "Load Page"
   - Start asking questions about the page content

## 🛠️ Project Structure

```
ANGBOT/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main Streamlit application
│   ├── pages/           # Additional pages
│   │   └── 1_Dashboard.py
│   ├── components/      # Reusable UI components
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── page_info.py
│   └── services/        # Business logic
│       ├── __init__.py
│       ├── confluence_service.py
│       └── openai_service.py
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in version control)
└── README.md          # This file
```

## 🤖 How It Works

1. The application connects to your Confluence instance using the provided API credentials
2. When you load a page, it fetches the content and processes it
3. When you ask a question, the system:
   - Uses OpenAI's GPT model to understand your question
   - Finds relevant information in the Confluence page
   - Generates a natural language response

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [OpenAI's GPT models](https://openai.com/)
- Integrates with [Atlassian Confluence Cloud API](https://developer.atlassian.com/cloud/confluence/rest/intro/)

## 📧 Contact

For any questions or feedback, please open an issue on GitHub.
