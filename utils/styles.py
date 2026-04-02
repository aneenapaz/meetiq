import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Import Professional Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main Background */
        .stApp {
            background-color: #FFFFFF !important;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E3F3FF !important;
            padding-top: 2rem !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #3E5A70 !important;
        }
        
        /* Sidebar Navigation Items */
        .sidebar-nav-item {
            padding: 12px 16px;
            margin: 4px 0;
            border-radius: 10px;
            transition: all 0.2s ease;
            cursor: pointer;
            color: #3E5A70;
            font-weight: 500;
        }
        
        .sidebar-nav-item:hover {
            background-color: #E3F3FF;
            transform: translateX(4px);
        }
        
        .sidebar-nav-item.active {
            background-color: #F9D5CE;
            color: #3E5A70;
            border-left: 3px solid #3E5A70;
        }
        
        /* Meeting Items in Sidebar */
        .meeting-item {
            padding: 12px 16px;
            margin: 6px 0;
            border-radius: 10px;
            transition: all 0.2s ease;
            cursor: pointer;
            border-left: 3px solid transparent;
        }
        
        .meeting-item:hover {
            background-color: #E3F3FF;
            transform: translateX(4px);
        }
        
        .meeting-item.selected {
            background-color: #F9D5CE;
            border-left-color: #3E5A70;
        }
        
        .meeting-title {
            font-weight: 600;
            font-size: 0.9rem;
            color: #3E5A70;
            margin-bottom: 4px;
        }
        
        .meeting-date {
            font-size: 0.75rem;
            color: #8A9AAC;
        }
        
        /* Section Headers */
        .section-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #3E5A70;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #E3F3FF;
        }
        
        /* Decision Cards */
        .decision-card {
            background-color: #E3F3FF;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid #3E5A70;
            transition: all 0.2s ease;
        }
        
        .decision-card:hover {
            transform: translateX(6px);
            box-shadow: 0 4px 12px rgba(62, 90, 112, 0.1);
        }
        
        .decision-text {
            color: #2C4A60;
            font-weight: 500;
            line-height: 1.5;
            margin: 0;
        }
        
        /* Action Items Table Styling */
        .action-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px;
        }
        
        .action-row {
            background-color: #FFFFFF;
            border-radius: 12px;
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .action-row:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(62, 90, 112, 0.1);
        }
        
        .action-cell {
            padding: 1rem;
            border-bottom: 1px solid #E3F3FF;
        }
        
        .responsible-badge {
            background-color: #F9D5CE;
            color: #3E5A70;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            display: inline-block;
        }
        
        .deadline-badge {
            background-color: #E3F3FF;
            color: #3E5A70;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            display: inline-block;
        }
        
        .deadline-urgent {
            background-color: #F9D5CE;
            color: #A05C4E;
        }
        
        /* Chatbot Panel */
        .chat-container {
            background-color: #FFFFFF;
            border-radius: 16px;
            border: 1px solid #E3F3FF;
            overflow: hidden;
        }
        
        .chat-header {
            background-color: #E3F3FF;
            padding: 1rem;
            border-bottom: 1px solid #D0E4F0;
        }
        
        .chat-header h4 {
            margin: 0;
            color: #3E5A70;
            font-weight: 600;
        }
        
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            padding: 1rem;
        }
        
        .user-message {
            background-color: #F9D5CE;
            color: #3E5A70;
            padding: 0.75rem 1rem;
            border-radius: 18px;
            border-bottom-right-radius: 4px;
            margin: 0.5rem 0;
            max-width: 85%;
            margin-left: auto;
            font-weight: 500;
        }
        
        .assistant-message {
            background-color: #E3F3FF;
            color: #3E5A70;
            padding: 0.75rem 1rem;
            border-radius: 18px;
            border-bottom-left-radius: 4px;
            margin: 0.5rem 0;
            max-width: 85%;
            font-weight: 400;
        }
        
        .citation-link {
            font-size: 0.75rem;
            color: #8A9AAC;
            margin-top: 0.5rem;
            cursor: pointer;
            text-decoration: underline;
        }
        
        /* Upload Area */
        .upload-area {
            background-color: #F0F7FF;
            border: 2px dashed #3E5A70;
            border-radius: 16px;
            padding: 3rem 2rem;
            text-align: center;
            transition: all 0.2s ease;
            margin: 2rem 0;
        }
        
        .upload-area:hover {
            background-color: #E3F3FF;
            border-color: #F9D5CE;
            transform: scale(1.01);
        }
        
        .upload-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        /* File Preview Cards */
        .file-preview {
            background-color: #FFFFFF;
            border: 1px solid #E3F3FF;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            transition: all 0.2s ease;
        }
        
        .file-preview:hover {
            box-shadow: 0 2px 8px rgba(62, 90, 112, 0.1);
        }
        
        .file-name {
            font-weight: 600;
            color: #3E5A70;
        }
        
        .file-meta {
            font-size: 0.8rem;
            color: #8A9AAC;
            margin-top: 0.5rem;
        }
        
        /* Stats Cards */
        .stat-card {
            background: linear-gradient(135deg, #E3F3FF 0%, #F0F7FF 100%);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            transition: all 0.2s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 16px rgba(62, 90, 112, 0.1);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 800;
            color: #3E5A70;
        }
        
        .stat-label {
            font-size: 0.85rem;
            color: #8A9AAC;
            margin-top: 0.5rem;
        }
        
        /* Buttons */
        .primary-button {
            background-color: #3E5A70;
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        .primary-button:hover {
            background-color: #2C4A60;
            transform: translateY(-1px);
        }
        
        .secondary-button {
            background-color: #F9D5CE;
            color: #3E5A70;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            border: none;
            font-weight: 500;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #3E5A70 !important;
        }
        
        p, span, div {
            color: #3E5A70;
        }
        
        /* Hide Streamlit Default Elements */
        header, footer, #MainMenu {
            visibility: hidden !important;
        }
        
        .stDeployButton {
            display: none !important;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #E3F3FF;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #F9D5CE;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #3E5A70;
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-fade-in {
            animation: fadeInUp 0.4s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)