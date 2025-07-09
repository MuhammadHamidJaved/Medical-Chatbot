import streamlit as st
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAI
import google.generativeai as genai
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

# Load environment variables
load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# Initialize components
@st.cache_resource
def initialize_components():
    # Initialize embeddings
    embeddings = download_hugging_face_embeddings()
    
    # Connect to existing Pinecone index
    index_name = "medicalbot"
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )
    
    # Create retriever
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
    
    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Initialize Gemini model
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.4,
        max_output_tokens=500,
        top_p=1,
        top_k=32,
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    
    # Create RAG chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

# Streamlit UI
def main():
    st.set_page_config(
        page_title=" Medical Bot",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("🏥 Medical Bot Assistant")
    st.markdown("### Ask me any medical questions and I'll help you with evidence-based answers!")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This Medical Bot uses:
        - 🤖 **Google Gemini AI** for intelligent responses
        - 📚 **Medical Knowledge Base** for accurate information
        - 🔍 **Semantic Search** for relevant context
        - 🔒 **Secure & Private** - no data stored
        """)
        
        st.header("⚙️ Settings")
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.4, 0.1)
        max_tokens = st.slider("Response Length", 100, 1000, 500, 50)
    
    # Initialize the RAG chain
    try:
        with st.spinner("🔄 Initializing Medical Bot..."):
            rag_chain = initialize_components()
        st.success("✅ Medical Bot is ready!")
    except Exception as e:
        st.error(f"❌ Error initializing bot: {str(e)}")
        st.stop()
    
    # Chat interface
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Medical Bot Assistant. How can I help you today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your medical question here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = rag_chain.invoke({"input": prompt})
                    answer = response["answer"]
                    
                    st.markdown(answer)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Show source documents in expander
                    if "context" in response:
                        with st.expander("📚 View Source Documents"):
                            for i, doc in enumerate(response.get("context", []), 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(doc.page_content[:300] + "...")
                                st.markdown("---")
                                
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == '__main__':
    main()