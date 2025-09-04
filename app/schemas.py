from typing import List, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1)
    stream: bool = False

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str

class EducateRequest(BaseModel):
    query: str
    top_k: int = 4

class SourceDoc(BaseModel):
    source: str
    snippet: str

class EducateResponse(BaseModel):
    answer: str
    sources: List[SourceDoc] = []

class MatchRequest(BaseModel):
    concerns: List[str] = Field(..., example=["anxiety", "sleep"])
    location: Optional[str] = None
    budget_range: Optional[str] = None

class Psychologist(BaseModel):
    name: str
    specialties: List[str]
    contact: Optional[str] = None
    location: Optional[str] = None

class MatchResponse(BaseModel):
    matches: List[Psychologist]
