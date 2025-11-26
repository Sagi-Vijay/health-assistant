# Health Assistant AI

An LLM-powered Health Assistance Application using Gemini 1.5 Pro, LangChain, FastAPI, and Streamlit.

## Prerequisites

- Python 3.9+
- Google API Key (for Gemini 1.5 Pro)

## Installation

1.  Clone the repository (or navigate to the project directory).
2.  Install dependencies:
    ```bash
    pip install fastapi uvicorn langchain langchain-google-genai langchain-community faiss-cpu sentence-transformers pydantic sqlalchemy python-multipart streamlit requests
    ```

## Setup

1.  Set your Google API Key as an environment variable:
    ```bash
    # Windows PowerShell
    $env:GOOGLE_API_KEY="your_api_key_here"
    
    # Linux/Mac
    export GOOGLE_API_KEY="your_api_key_here"
    ```

## Running the Application

You need to run the Backend and Frontend in separate terminals.

### 1. Start the Backend
```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Start the Frontend
```bash
streamlit run frontend/app.py
```
The UI will open in your browser at `http://localhost:8501`.

## Features

- **Symptom Analysis**: Describe your symptoms and get a structured analysis.
- **Diagnosis Suggestion**: RAG-powered suggestions based on medical knowledge (Dummy data for demo).
- **Chat Interface**: Ask general health questions.
- **Safety Guardrails**: The system refuses to give specific prescriptions and always includes disclaimers.
