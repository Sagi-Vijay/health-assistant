# 🩺 AI Health Assistant

[![CI](https://github.com/Sagi-Vijay/health-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/Sagi-Vijay/health-assistant/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

> **An advanced, AI-powered healthcare companion built with Gemini 1.5 Pro, LangChain, and FastAPI.**

The **AI Health Assistant** is a comprehensive platform designed to provide preliminary health insights, symptom analysis, and medical knowledge retrieval. It leverages the power of Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to deliver accurate, context-aware responses while maintaining strict safety guardrails.

---

## 🚀 Features

### 🧠 Intelligent Analysis
-   **Symptom Checker**: Describe your symptoms in natural language, and the AI will extract key indicators, estimate severity, and suggest potential conditions.
-   **RAG-Powered Diagnosis**: Uses a vector database of medical knowledge to ground its suggestions in verified medical texts (demonstration data included).
-   **Medical Report Analysis**: Upload PDF lab reports or prescriptions. The system parses the document and summarizes key findings using OCR and LLM analysis.

### 🗣️ Multimodal Interaction
-   **Voice Assistant**: Speak your symptoms! The system accepts audio input, transcribes it, and provides an instant analysis.
-   **Chat Interface**: A conversational agent that remembers your session context for follow-up questions.

### 🛡️ Secure & Personalized
-   **User Authentication**: Secure Signup/Login using JWT (JSON Web Tokens).
-   **Medical History**: All your interactions are securely stored. Review your past queries and AI responses anytime.
-   **Doctor Dashboard**: A dedicated view for healthcare professionals to review patient interaction summaries (Demo mode).

---

## 🛠️ Tech Stack

-   **LLM**: [Google Gemini 1.5 Pro](https://deepmind.google/technologies/gemini/) (via Google AI Studio)
-   **Orchestration**: [LangChain](https://langchain.com/)
-   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Python API)
-   **Frontend**: [Streamlit](https://streamlit.io/) (Interactive Data App)
-   **Vector DB**: [FAISS](https://github.com/facebookresearch/faiss) (Local vector store for RAG)
-   **Database**: SQLite (with SQLAlchemy ORM)
-   **Auth**: OAuth2 with Password hashing (Bcrypt) & JWT

---

## 📦 Installation

### Prerequisites
-   Python 3.9 or higher
-   A Google API Key (Get it [here](https://aistudio.google.com/app/apikey))

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Sagi-Vijay/health-assistant.git
    cd health-assistant
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Environment Variables**
    Set your Google API Key.
    -   **Windows (PowerShell)**: `$env:GOOGLE_API_KEY="your_key_here"`
    -   **Linux/Mac**: `export GOOGLE_API_KEY="your_key_here"`

---

## 🏃‍♂️ Usage

You need to run the Backend and Frontend in separate terminals.

### 1. Start the Backend Server
```bash
uvicorn backend.main:app --reload
```
*The API will be live at `http://localhost:8000`*

### 2. Start the Frontend UI
```bash
streamlit run frontend/app.py
```
*The App will open in your browser at `http://localhost:8501`*

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request


---

