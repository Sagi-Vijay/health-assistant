import os
import shutil
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.models import SymptomAnalysisRequest, SymptomAnalysisResponse, ChatRequest, ChatResponse, UserCreate, User, Token, InteractionLog
from backend.rag_pipeline import initialize_rag_pipeline, get_retriever
from backend.chains import get_symptom_chain, get_diagnosis_chain, get_chat_chain
from backend.database import init_db, get_db, Interaction, User as DBUser
from backend.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.document_processor import process_pdf
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import json

app = FastAPI(title="Health Assistant AI")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from jose import JWTError, jwt
    from backend.auth import SECRET_KEY, ALGORITHM
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = DBUser(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
async def analyze_symptoms(request: SymptomAnalysisRequest, current_user: User = Depends(get_current_user)):
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
async def diagnose(request: SymptomAnalysisRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
            llm_response=response,
            user_id=current_user.id
        )
        db.add(interaction)
        db.commit()
        
        return {"diagnosis_suggestion": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        retriever = get_retriever()
        chain = get_chat_chain(retriever)
        
        response = chain.run(request.message)
        
        # Log interaction
        interaction = Interaction(
            session_id=request.session_id,
            user_query=request.message,
            llm_response=response,
            user_id=current_user.id
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

@app.get("/history", response_model=List[InteractionLog])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    interactions = db.query(Interaction).filter(Interaction.user_id == current_user.id).all()
    return interactions

@app.post("/upload_report")
async def upload_report(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    try:
        # Save file temporarily
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        # Process PDF
        retriever = process_pdf(file_location)
        
        # Analyze with RAG (using Diagnosis Chain for now as a generic analyzer)
        chain = get_diagnosis_chain(retriever)
        response = chain.run("Analyze this medical report and summarize key findings.")
        
        # Cleanup
        os.remove(file_location)
        
        return {"analysis": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
