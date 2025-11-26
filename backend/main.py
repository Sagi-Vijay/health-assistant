import os
from fastapi import FastAPI, HTTPException, Depends
from backend.models import SymptomAnalysisRequest, SymptomAnalysisResponse, ChatRequest, ChatResponse
from backend.rag_pipeline import initialize_rag_pipeline, get_retriever
from backend.chains import get_symptom_chain, get_diagnosis_chain, get_chat_chain
from backend.database import init_db, get_db, Interaction
from sqlalchemy.orm import Session
import json

app = FastAPI(title="Health Assistant AI")

# Initialize RAG and DB on startup
@app.on_event("startup")
async def startup_event():
    # Initialize DB
    init_db()
    
    # Initialize RAG Pipeline
    # Assuming data is in ../data/medical_knowledge.txt relative to this file
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "medical_knowledge.txt")
    initialize_rag_pipeline(data_path)

@app.get("/")
async def root():
    return {"message": "Health Assistant AI API is running"}

@app.post("/analyze_symptoms", response_model=SymptomAnalysisResponse)
async def analyze_symptoms(request: SymptomAnalysisRequest):
    try:
        chain = get_symptom_chain()
        result = chain.run(request.user_input)
        
        # Parse JSON from LLM response (it might be wrapped in markdown code blocks)
        cleaned_result = result.replace("```json", "").replace("```", "").strip()
        parsed_result = json.loads(cleaned_result)
        
        return SymptomAnalysisResponse(**parsed_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diagnose")
async def diagnose(request: SymptomAnalysisRequest, db: Session = Depends(get_db)):
    try:
        # 1. Extract symptoms first (optional, but good for structured input)
        # For now, we just use the raw input as "symptoms" for the RAG chain
        
        retriever = get_retriever()
        chain = get_diagnosis_chain(retriever)
        
        # The chain expects "symptoms" as input key because we defined it in the prompt
        # But RetrievalQA usually expects "query". We might need to adjust or use "query" as the input key.
        # Let's adjust the chain call. RetrievalQA by default uses "query".
        # We will pass the user input as the query.
        
        response = chain.run(request.user_input)
        
        # Log interaction
        interaction = Interaction(
            session_id="test_session", # In real app, get from auth/header
            user_query=request.user_input,
            llm_response=response
        )
        db.add(interaction)
        db.commit()
        
        return {"diagnosis_suggestion": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        retriever = get_retriever()
        chain = get_chat_chain(retriever)
        
        response = chain.run(request.message)
        
        # Log interaction
        interaction = Interaction(
            session_id=request.session_id,
            user_query=request.message,
            llm_response=response
        )
        db.add(interaction)
        db.commit()
        
        return ChatResponse(
            response=response,
            context_used=[], # Placeholder, would need to extract source docs from chain result
            safety_warning=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
