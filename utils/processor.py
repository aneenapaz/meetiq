import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import re
import streamlit as st

load_dotenv()

def get_api_key():
    try:
        if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
            return st.secrets['GROQ_API_KEY']
    except:
        pass
    return os.getenv('GROQ_API_KEY')

def process_transcript(text):
    api_key = get_api_key()
    
    if not api_key:
        # Demo mode - return sample response
        return {
            "decisions": [
                "Demo Mode: Add API key for full extraction",
                "Upload your transcript to see real decisions",
                "Contact developer for access"
            ],
            "action_items": [
                {"Responsible": "User", "Task": "Add GROQ_API_KEY to .env or secrets", "Deadline": "Now"},
                {"Responsible": "Developer", "Task": "Configure API key for full functionality", "Deadline": "Ongoing"}
            ]
        }
    
    # Truncate text if too long
    max_chars = 6000
    if len(text) > max_chars:
        text = text[:max_chars] + "... [transcript truncated]"
    
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.3-70b-versatile",
        groq_api_key=api_key
    )
    
    prompt = f"""Analyze this meeting transcript and extract:

1. Key Decisions: Things the team agreed on (list as bullet points)
2. Action Items: Tasks assigned to people - include WHO is responsible, WHAT they need to do, and BY WHEN

Format your response EXACTLY like this:

DECISIONS:
- Decision 1
- Decision 2
- Decision 3

ACTION ITEMS:
- WHO: Person Name | WHAT: Task description | BY WHEN: Deadline
- WHO: Person Name | WHAT: Task description | BY WHEN: Deadline

Transcript:
{text}
"""
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        
        # Parse decisions
        decisions = []
        decisions_match = re.search(r'DECISIONS:\n(.*?)(?=\n\nACTION ITEMS:|\nACTION ITEMS:|$)', content, re.DOTALL | re.IGNORECASE)
        if decisions_match:
            decisions_text = decisions_match.group(1)
            for line in decisions_text.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('*'):
                    decisions.append(line.lstrip('-* ').strip())
                elif line and not line.startswith('ACTION'):
                    decisions.append(line)
        
        # Parse action items
        action_items = []
        action_match = re.search(r'ACTION ITEMS:\n(.*?)(?=\n\n|\Z)', content, re.DOTALL | re.IGNORECASE)
        if action_match:
            action_text = action_match.group(1)
            action_pattern = r'WHO:\s*([^|]+)\|\s*WHAT:\s*([^|]+)\|\s*BY WHEN:\s*([^\n]+)'
            matches = re.findall(action_pattern, action_text, re.IGNORECASE)
            
            for match in matches:
                action_items.append({
                    "Responsible": match[0].strip(),
                    "Task": match[1].strip(),
                    "Deadline": match[2].strip()
                })
        
        # Clean up decisions
        decisions = [d for d in decisions if d and len(d) > 5]
        
        # Ensure we have at least some data
        if not decisions:
            decisions = ["No clear decisions identified in this transcript"]
        
        if not action_items:
            action_items = [{"Responsible": "Team", "Task": "Review transcript for action items", "Deadline": "Ongoing"}]
        
        return {
            "decisions": decisions[:5],
            "action_items": action_items[:10]
        }
        
    except Exception as e:
        print(f"Error processing transcript: {str(e)}")
        return {
            "decisions": [f"Error processing transcript: {str(e)}"], 
            "action_items": []
        }