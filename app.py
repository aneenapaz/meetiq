import streamlit as st
import pandas as pd
import os
import re
import base64
from datetime import datetime
from utils.styles import apply_custom_css
from utils.processor import process_transcript 
from utils.chatbot import run_query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(page_title="MeetIQ", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if "files" not in st.session_state:
    st.session_state.files = None
if "current_meeting_index" not in st.session_state:
    st.session_state.current_meeting_index = None
if "meeting_history" not in st.session_state:
    st.session_state.meeting_history = []
if "processed_data" not in st.session_state:
    st.session_state.processed_data = {}
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# Function to encode image to base64 for CSS (Stops Flickering)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_base64 = get_base64_image("assets/illustration.png")

# Helper functions
def extract_meeting_name(content):
    patterns = [r'MEETING:\s*(.+?)(?:\n|$)', r'Meeting Title:\s*(.+?)(?:\n|$)', r'Topic:\s*(.+?)(?:\n|$)']
    for p in patterns:
        match = re.search(p, content, re.IGNORECASE)
        if match: return match.group(1).strip()
    return None

def get_meeting_stats(content):
    words = len(content.split())
    speakers = len(re.findall(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\s*:', content, re.MULTILINE))
    return words, max(speakers, 1)

def detect_meeting_date(content):
    match = re.search(r'DATE:\s*([A-Z][a-z]+ \d{1,2},? \d{4})', content, re.IGNORECASE)
    return match.group(1) if match else datetime.now().strftime("%b %d, %Y")

# Custom CSS
st.markdown(f"""
    <style>
        /* Force Sidebar Open */
        [data-testid="stSidebar"] {{ min-width: 280px !important; width: 280px !important; background-color: #F9F7F5 !important; }}
        [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
        
        /* ANTIFLICKER IMAGE BOX */
        .flicker-free-img {{
            width: 100%;
            height: 400px;
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center right;
        }}

        /* Chat Styling */
        .user-message {{ background-color: #F9D5CE; color: #3E5A70; padding: 0.75rem 1rem; border-radius: 18px 18px 4px 18px; margin: 0.5rem 0 0.5rem auto; width: fit-content; max-width: 85%; font-weight: 500; }}
        .assistant-message {{ background-color: #E3F3FF; color: #3E5A70; padding: 0.75rem 1rem; border-radius: 18px 18px 18px 4px; margin: 0.5rem 0; width: fit-content; max-width: 85%; }}
        
        /* Cards */
        .decision-card {{ background-color: #E3F3FF; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; border-left: 4px solid #3E5A70; font-weight: 500; color: #2C4A60; }}
        .action-card {{ background-color: #FFFFFF; border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem; border: 1px solid #E3F3FF; }}
        .responsible-badge {{ background-color: #F9D5CE; color: #3E5A70; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }}
        .deadline-badge {{ background-color: #E3F3FF; color: #3E5A70; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; }}
        
        /* Sidebar Stats */
        .stat-card {{ background: linear-gradient(135deg, #E3F3FF 0%, #F0F7FF 100%); border-radius: 12px; padding: 1rem; text-align: center; }}
        .stat-number {{ font-size: 1.5rem; font-weight: 800; color: #3E5A70; }}
        .stat-label {{ font-size: 0.75rem; color: #8A9AAC; }}
        
        .section-header {{ font-size: 1.5rem; font-weight: 700; color: #3E5A70; margin: 1.5rem 0 1rem 0; border-bottom: 2px solid #E3F3FF; padding-bottom: 5px; }}
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<h2 style="color: #3E5A70; margin-bottom:0;">MeetIQ</h2><p style="color: #8A9AAC;">Meeting Intelligence Hub</p>', unsafe_allow_html=True)
    if st.button("+ New Upload", use_container_width=True):
        st.session_state.files = None
        st.session_state.current_meeting_index = None
        st.rerun()
    
    st.markdown('<hr style="border-color: #E3F3FF;">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #3E5A70;">Meetings</h4>', unsafe_allow_html=True)
    
    for idx, meeting in enumerate(st.session_state.meeting_history):
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(meeting['display_name'][:25], key=f"m_{idx}", use_container_width=True):
                st.session_state.current_meeting_index = idx
                st.session_state.files = [meeting['file_obj']]
                st.rerun()
        with col2:
            if st.button("✕", key=f"del_{idx}"):
                st.session_state.meeting_history.pop(idx)
                st.rerun()
        st.markdown(f'<p style="font-size: 0.75rem; color: #8A9AAC; margin:-10px 0 10px 5px;">{meeting["date"]}</p>', unsafe_allow_html=True)

    if st.session_state.meeting_history:
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        total_actions = sum(len(st.session_state.processed_data.get(m['name'], {}).get('action_items', [])) for m in st.session_state.meeting_history)
        c1.markdown(f'<div class="stat-card"><div class="stat-number">{len(st.session_state.meeting_history)}</div><div class="stat-label">Meetings</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="stat-card"><div class="stat-number">{total_actions}</div><div class="stat-label">Actions</div></div>', unsafe_allow_html=True)

# Main Content
if st.session_state.files is None:
    col1, col2 = st.columns([6, 5], gap="large")
    with col1:
        st.markdown('<h1 style="color: #3E5A70;">MeetIQ</h1>', unsafe_allow_html=True)
        st.markdown('''
            <p style="font-size: 1.1rem; color: #8A9AAC; margin-bottom: 2rem;">
            Transform meeting transcripts into actionable intelligence.<br>
            Extract decisions, track action items, and get answers instantly.
            </p>
        ''', unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader("", type=['txt', 'vtt'], accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                if not any(m['name'] == file.name for m in st.session_state.meeting_history):
                    content = file.getvalue().decode("utf-8")
                    with st.spinner(f"Processing {file.name}..."):
                        w, s = get_meeting_stats(content)
                        display_name = extract_meeting_name(content) or file.name.replace('.txt', '').replace('.vtt', '')
                        st.session_state.meeting_history.append({
                            'name': file.name, 'display_name': display_name,
                            'date': detect_meeting_date(content), 'words': w, 'speakers': s, 'file_obj': file
                        })
                        st.session_state.processed_data[file.name] = process_transcript(content)
            
            if st.session_state.meeting_history:
                st.session_state.current_meeting_index = 0
                st.session_state.files = [st.session_state.meeting_history[0]['file_obj']]
                st.rerun()
    with col2:
        # Use the flicker-free CSS container instead of st.image
        st.markdown('<div class="flicker-free-img"></div>', unsafe_allow_html=True)

else:
    curr = st.session_state.meeting_history[st.session_state.current_meeting_index]
    data = st.session_state.processed_data.get(curr['name'], {"decisions": [], "action_items": []})
    
    col_main, col_chat = st.columns([2.2, 1.2], gap="large")
    
    with col_main:
        st.markdown(f'<h2 style="color: #3E5A70; margin-bottom:10px;">{curr["display_name"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'''<div style="display:flex; gap:10px; margin-bottom:20px;">
            <span style="background:#E3F3FF; padding:4px 12px; border-radius:12px; font-size:0.85rem;">📅 {curr["date"]}</span>
            <span style="background:#E3F3FF; padding:4px 12px; border-radius:12px; font-size:0.85rem;">👥 {curr["speakers"]} speakers</span>
            <span style="background:#E3F3FF; padding:4px 12px; border-radius:12px; font-size:0.85rem;">📝 {curr["words"]} words</span>
        </div>''', unsafe_allow_html=True)
        
        st.markdown('<h3 class="section-header">Key Decisions</h3>', unsafe_allow_html=True)
        for d in data.get('decisions', []):
            st.markdown(f'<div class="decision-card">{d}</div>', unsafe_allow_html=True)
        
        st.markdown('<h3 class="section-header">Action Items</h3>', unsafe_allow_html=True)
        actions = data.get('action_items', [])
        for a in actions:
            st.markdown(f'''<div class="action-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div><span class="responsible-badge">{a.get('Responsible', 'Unassigned')}</span><p style="margin:10px 0 0 0; font-weight:500;">{a.get('Task', '')}</p></div>
                    <span class="deadline-badge">📅 {a.get('Deadline', 'N/A')}</span>
                </div></div>''', unsafe_allow_html=True)
        
        if actions:
            csv = pd.DataFrame(actions).to_csv(index=False).encode('utf-8')
            st.download_button("Export as CSV", data=csv, file_name=f"{curr['display_name']}_actions.csv", use_container_width=True)

    with col_chat:
        st.markdown('<div style="background:#E3F3FF; padding:15px; border-radius:15px 15px 0 0; border:1px solid #D0E4F0; color:#3E5A70;"><b>Meeting Assistant</b><br><small style="color:#8A9AAC;">Ask questions about this meeting</small></div>', unsafe_allow_html=True)
        with st.container(height=450, border=True):
            for m in st.session_state.chat_messages:
                st.markdown(f'<div class="{"user-message" if m["role"]=="user" else "assistant-message"}">{m["content"]}</div>', unsafe_allow_html=True)
        
        with st.form(key="chat_f", clear_on_submit=True):
            q = st.text_input("", placeholder="Ask a question about this meeting...", label_visibility="collapsed")
            if st.form_submit_button("Send", use_container_width=True) and q:
                st.session_state.chat_messages.append({'role': 'user', 'content': q})
                with st.spinner("Thinking..."):
                    ans, docs = run_query(q, curr['file_obj'].getvalue().decode("utf-8"), curr['display_name'])
                    if docs and "Source:" not in ans and "[" not in ans:
                        unique = sorted(list(set([d.metadata.get('source', 'Unknown') for d in docs])))
                        ans += "\n\n**Sources:**\n" + "\n".join([f"- {s}" for s in unique])
                    st.session_state.chat_messages.append({'role': 'assistant', 'content': ans})
                st.rerun()