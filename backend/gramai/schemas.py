from typing import Any, Optional

from pydantic import BaseModel, Field


class AssessmentCreate(BaseModel):
    village: str = Field(min_length=1)
    block: str = Field(min_length=1)
    district: str = Field(min_length=1)
    state: str = Field(min_length=1)
    available_capital: float = Field(gt=0)
    business_category: str = Field(min_length=1)
    experience: Optional[str] = None
    skills: Optional[str] = None
    preferred_business_size: Optional[str] = None


class AnalyzeRequest(BaseModel):
    assessment_id: int = Field(gt=0)


class FinancialPlanRequest(BaseModel):
    assessment_id: Optional[int] = Field(default=None, gt=0)
    available_capital: Optional[float] = Field(default=None, gt=0)


class SchemeRecommendationRequest(BaseModel):
    project_cost: float = Field(gt=0)
    calculated_financing: Optional[float] = Field(default=None, ge=0)


class AssessmentResponse(BaseModel):
    assessment_id: int
    status: str
    prototype_label: str = "Prototype data / AI estimate"


class AnalysisResponse(BaseModel):
    assessment_id: int
    mode: str
    analysis: dict[str, Any]
    financial_plan: dict[str, Any]
    scheme_recommendation: dict[str, Any]
    final_recommendation: dict[str, Any]