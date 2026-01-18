from pydantic import BaseModel
from typing import List, Optional

class IdeaRequest(BaseModel):
    idea: str

class QuestionRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    response: str
    evaluation: Optional[str] = None
    references: Optional[List[dict]] = None
    idea_score: Optional[int] = None
