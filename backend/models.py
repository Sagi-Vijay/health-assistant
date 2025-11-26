from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SymptomAnalysisRequest(BaseModel):
    user_input: str

class SymptomAnalysisResponse(BaseModel):
    symptoms: List[str]
    severity: str
    duration: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    context_used: List[str]
    safety_warning: bool = False

class InteractionLog(BaseModel):
    id: int
    session_id: str
    user_query: str
    llm_response: str
    timestamp: datetime
