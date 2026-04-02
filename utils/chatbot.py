import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st

load_dotenv()

def get_api_key():
    try:
        if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
            return st.secrets['GROQ_API_KEY']
    except:
        pass
    return os.getenv('GROQ_API_KEY')

def run_query(query, file_content, file_name):
    api_key = get_api_key()
    
    if not api_key:
        return "⚠️ Demo Mode: Add GROQ_API_KEY to enable full chatbot functionality. The AI assistant will answer questions about your meetings once configured.", []
    
    if not file_content or len(file_content) < 50:
        return "The transcript content is too short or empty to search through.", []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_text(file_content)
    
    if not chunks:
        return "No content found to search through.", []
    
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_texts(chunks, embeddings, metadatas=[{"source": file_name, "chunk_id": i} for i in range(len(chunks))])
        
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            groq_api_key=api_key, 
            temperature=0
        )
        
        docs = vector_db.similarity_search(query, k=3)
        
        if not docs:
            return "No relevant information found in the transcripts.", []
        
        context_parts = []
        for i, doc in enumerate(docs):
            context_parts.append(f"[Source: {doc.metadata['source']}, Section {doc.metadata['chunk_id']}]\n{doc.page_content}")
        
        context = "\n---\n".join(context_parts)
        
        prompt = f"""You are analyzing meeting transcripts. Answer the question based ONLY on the context below.

Context:
{context}

Question: {query}

Instructions:
1. Answer directly and concisely
2. If the exact answer isn't in the context, say "Based on available transcripts, I cannot find information about {query}"
3. Always cite which meeting or section the information comes from
4. For speaker questions, identify the speaker if mentioned

Answer:"""
        
        response = llm.invoke(prompt)
        return response.content, docs
        
    except Exception as e:
        print(f"Error in chatbot query: {str(e)}")
        return f"Error processing query: {str(e)}", []