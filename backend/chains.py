import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RetrievalQA
from langchain.schema import SystemMessage

# Ensure API key is set
if "GOOGLE_API_KEY" not in os.environ:
    # Fallback for development if not set in env, though user should set it.
    print("WARNING: GOOGLE_API_KEY not found in environment variables.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)

# --- Prompts ---

SYMPTOM_ANALYSIS_TEMPLATE = """
Analyze the following user input and extract the symptoms.
User Input: {user_input}

Return the output in the following JSON format:
{{
    "symptoms": ["list", "of", "symptoms"],
    "severity": "low/medium/high",
    "duration": "string or null"
}}
"""

DIAGNOSIS_TEMPLATE = """
You are an AI health assistant. You do NOT provide medical diagnosis or prescriptions. 
Always advise seeing a doctor.

Context:
{context}

User Symptoms: {symptoms}

Based on the context provided, suggest possible conditions that match the symptoms.
DISCLAIMER: State clearly that this is not a medical diagnosis.

Format:
- Condition 1: Explanation (Confidence: Low/Medium)
- Condition 2: Explanation
"""

CHAT_TEMPLATE = """
You are a helpful AI health assistant.
Context:
{context}

User Question: {question}

Answer the question based on the context. If the answer is not in the context, say you don't know.
Do NOT provide medical advice or prescriptions.
"""

# --- Chains ---

def get_symptom_chain():
    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=SYMPTOM_ANALYSIS_TEMPLATE
    )
    return LLMChain(llm=llm, prompt=prompt)

def get_diagnosis_chain(retriever):
    prompt = PromptTemplate(
        input_variables=["context", "symptoms"],
        template=DIAGNOSIS_TEMPLATE
    )
    # Using RetrievalQA for RAG
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

def get_chat_chain(retriever):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=CHAT_TEMPLATE
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain
