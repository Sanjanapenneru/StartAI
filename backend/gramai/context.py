from typing import Any, Dict, List, TypedDict


class EntrepreneurContext(TypedDict, total=False):
    assessment_id: int
    village: str
    block: str
    district: str
    state: str
    available_capital: float
    business_category: str
    experience: str
    skills: str
    preferred_business_size: str
    market_analysis: Dict[str, Any]
    competition_analysis: Dict[str, Any]
    feasibility_analysis: Dict[str, Any]
    financial_plan: Dict[str, Any]
    scheme_recommendation: Dict[str, Any]
    final_recommendation: Dict[str, Any]
    ai_mode: str
    completed_agents: List[str]