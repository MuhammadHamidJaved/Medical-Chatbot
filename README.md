# 🏥 Medical Bot - Streamlit Version

A modern medical assistant powered by Google Gemini AI and medical knowledge base.

## 🚀 Features

- **🤖 Google Gemini AI**: Latest AI technology for intelligent responses
- **📚 Medical Knowledge Base**: Evidence-based medical information
- **🔍 Semantic Search**: Relevant context retrieval using Pinecone
- **💬 Chat Interface**: Modern, user-friendly Streamlit interface
- **🔒 Secure**: No personal data stored

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit the `.env` file and add your API keys:
```
PINECONE_API_KEY=your_pinecone_key_here
GEMINI_API_KEY=your_gemini_key_here
```

**Get your API keys:**
- Gemini API: https://ai.google.dev/
- Pinecone: https://www.pinecone.io/

### 3. Run the Application

**Option 1: Using the run script**
```bash
python run_app.py
```

**Option 2: Direct Streamlit command**
```bash
streamlit run app.py --server.port 8080
```

### 4. Access the App
Open your browser and go to: `http://localhost:8080`

## 🔧 Architecture

```
User Question → Streamlit UI → Embeddings → Pinecone Search → Gemini AI → Response
```

## 📦 Key Components

- **`app.py`**: Main Streamlit application
- **`src/helper.py`**: Utility functions for embeddings
- **`src/prompt.py`**: System prompts for AI
- **`.env`**: Environment variables (API keys)
- **`requirements.txt`**: Python dependencies

## 🎯 Usage

1. Open the web interface
2. Type your medical question in the chat
3. Get AI-powered responses with source references
4. View source documents for transparency

## 🔄 Migration from Flask

- ✅ Replaced Flask with Streamlit
- ✅ Switched from OpenAI to Gemini
- ✅ Added modern chat interface
- ✅ Improved error handling
- ✅ Added source document display

## 🐛 Troubleshooting

1. **API Key Issues**: Verify your `.env` file has correct keys
2. **Package Errors**: Run `pip install -r requirements.txt`
3. **Port Issues**: Change port in run command if 8080 is busy

## 💡 Benefits of New Version

- 🆓 **Cost Effective**: Gemini has generous free tier
- ⚡ **Faster**: Better performance than previous version
- 🎨 **Modern UI**: Beautiful Streamlit interface
- 📱 **Responsive**: Works on mobile and desktop
- 🔧 **Easy Setup**: Simple installation and configuration
