# MeetIQ - Meeting Intelligence Hub

## The Problem

Every organization holds dozens of meetings weekly, generating hours of audio and video content. While speech-to-text tools can convert these meetings into transcripts, a single one-hour meeting produces 20+ pages of text. Stakeholders rarely have time to read through these lengthy documents to find key decisions, action items, or the reasoning behind important strategies. This creates "double work" where team members waste time asking "What happened in that meeting?" instead of executing tasks.

## The Solution

MeetIQ is an intelligent meeting analysis platform that automatically extracts structured insights from meeting transcripts. The solution provides:

- **Decision & Action Item Extraction**: Automatically identifies key decisions made during meetings and extracts action items with three critical components: Who is responsible, What they need to do, and By When it should be completed.

- **Contextual Query Chatbot**: A conversational AI interface that allows users to ask natural language questions across uploaded transcripts. The chatbot understands context, handles speaker-specific questions, and always cites its sources (which meeting and which section the answer came from).

- **Multi-Transcript Management**: Upload and organize multiple meeting transcripts with automatic detection of meeting dates, speaker counts, and word counts for easy reference.

- **Export Capabilities**: Export extracted action items as CSV files for integration with project management tools.

## Tech Stack

### Programming Languages
- Python 3.9+

### Frameworks & Libraries
- **Streamlit** - Web application framework for the user interface
- **LangChain** - Framework for LLM orchestration and chain management
- **LangChain-Groq** - Groq API integration for LLM access

### AI & Machine Learning
- **Groq LLM** (llama-3.3-70b-versatile) - Large language model for transcript analysis and Q&A
- **HuggingFace Embeddings** (all-MiniLM-L6-v2) - Sentence embeddings for semantic search
- **FAISS** - Vector database for efficient similarity search

### Data Processing
- **Pandas** - Data manipulation and CSV export
- **python-dotenv** - Environment variable management

### Natural Language Processing
- **Sentence-Transformers** - Text embedding generation
- **LangChain Text Splitters** - Intelligent text chunking for long documents

## Setup Instructions

### Prerequisites

- Python 3.9 or higher installed
- Groq API key (get one free at [console.groq.com](https://console.groq.com))

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-username/meetiq.git
cd meetiq