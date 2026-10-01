from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
class Decision(BaseModel):
    description: str

class ActionItem(BaseModel):
    task: str
    assignee: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class Risk(BaseModel):
    description: str

class Blocker(BaseModel):
    description: str

class unresolvedItem(BaseModel):
    item: str

class MeetingAnalysis(BaseModel):
    summary:str

    decision:list[Decision] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    blockers: list[Blocker] = Field(default_factory=list)
    unresolved_items: list[unresolvedItem] = Field(default_factory=list)
    participants: list[str] = Field(default_factory=list)

class MeetingCreate(BaseModel):
    filename: str

class MettingResponce(BaseModel):
    id: str
    filename: str
    status: str
    transcript: Optional[str] = None
    analysis: Optional[MeetingAnalysis] = None
    created_at: datetime

class MeetingQueryRequest(BaseModel):
    question: str = Field(..., min_length = 1, max_length = 1000)

class MeetingQueryResponce(BaseModel):
    question: str
    answer: str
    