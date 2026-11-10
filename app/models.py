from typing import Optional

from pydantic import BaseModel, Field


class OrchestrationRequest(BaseModel):
    question: str = Field(..., min_length=3, description="User request that needs routing")


class OrchestrationResponse(BaseModel):
    classification: str
    output_type: str
    summary: str
    reasoning: str
    generated_code: Optional[str] = None
    impact_summary: Optional[str] = None
    recommended_approach: Optional[str] = None
