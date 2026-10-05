from pydantic import BaseModel, Field

class SupportRequest(BaseModel):
    issue: str = Field(min_length=3)

class SupportAnswer(BaseModel):
    category: str
    diagnosis: str
    likely_cause: str
    recommended_fix: str
    confidence: float
    evidence: list[str]
    files_checked: list[str]
