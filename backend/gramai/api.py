from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from gramai.finance import calculate_financial_plan, recommend_scheme
from gramai.schemas import (
    AnalysisResponse,
    AssessmentCreate,
    AssessmentResponse,
    AnalyzeRequest,
    FinancialPlanRequest,
    SchemeRecommendationRequest,
)
from gramai.workflow import build_workflow
from models.startup_models import (
    BusinessAnalysis,
    EntrepreneurAssessment,
    FinancialPlan,
    SchemeRecommendation,
)
from services.auth_dependency import get_optional_user
from services.database import SessionLocal

router = APIRouter(prefix="/api", tags=["GRAMAI"])


def _db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _assessment_context(assessment: EntrepreneurAssessment) -> dict:
    return {
        "assessment_id": assessment.id,
        "village": assessment.village,
        "block": assessment.block,
        "district": assessment.district,
        "state": assessment.state,
        "available_capital": assessment.available_capital,
        "business_category": assessment.business_category,
        "experience": assessment.experience or "",
        "skills": assessment.skills or "",
        "preferred_business_size": assessment.preferred_business_size or "",
        "completed_agents": [],
    }


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "GRAMAI",
        "demo_mode_available": True,
    }


@router.post("/assessment", response_model=AssessmentResponse)
def create_assessment(
    data: AssessmentCreate,
    db: Session = Depends(_db),
    current_user: dict | None = Depends(get_optional_user),
):
    assessment = EntrepreneurAssessment(
        **data.dict(),
        user_uid=current_user["uid"] if current_user else None,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return {"assessment_id": assessment.id, "status": assessment.status}


@router.post("/analyze", response_model=AnalysisResponse)
def analyze(
    data: AnalyzeRequest,
    db: Session = Depends(_db),
    current_user: dict | None = Depends(get_optional_user),
):
    assessment = (
        db.query(EntrepreneurAssessment)
        .filter(EntrepreneurAssessment.id == data.assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")
    if current_user and assessment.user_uid and assessment.user_uid != current_user["uid"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this assessment.",
        )

    try:
        state = build_workflow().invoke(_assessment_context(assessment))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Analysis is temporarily unavailable. Please try again.",
        ) from exc

    analysis_row = BusinessAnalysis(
        assessment_id=assessment.id,
        result=state["feasibility_analysis"],
        mode=state.get("ai_mode", "demo"),
    )
    financial_row = FinancialPlan(
        assessment_id=assessment.id,
        result=state["financial_plan"],
    )
    scheme_row = SchemeRecommendation(
        assessment_id=assessment.id,
        result=state["scheme_recommendation"],
    )
    assessment.status = "analyzed"
    db.add_all([analysis_row, financial_row, scheme_row])
    db.commit()

    return {
        "assessment_id": assessment.id,
        "mode": (
            "Gemini"
            if state.get("ai_mode") == "gemini"
            else "Prototype Demo Mode"
        ),
        "analysis": {
            "market": state["market_analysis"],
            "competition": state["competition_analysis"],
            "feasibility": state["feasibility_analysis"],
        },
        "financial_plan": state["financial_plan"],
        "scheme_recommendation": state["scheme_recommendation"],
        "final_recommendation": state["final_recommendation"],
    }


@router.post("/financial-plan")
def financial_plan(
    data: FinancialPlanRequest,
    db: Session = Depends(_db),
    current_user: dict | None = Depends(get_optional_user),
):
    capital = data.available_capital
    assessment = None

    if data.assessment_id:
        assessment = (
            db.query(EntrepreneurAssessment)
            .filter(EntrepreneurAssessment.id == data.assessment_id)
            .first()
        )
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found.")
        if current_user and assessment.user_uid and assessment.user_uid != current_user["uid"]:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this assessment.",
            )
        capital = assessment.available_capital

    if capital is None:
        raise HTTPException(
            status_code=422,
            detail="Provide assessment_id or available_capital.",
        )

    try:
        result = calculate_financial_plan(capital)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if assessment:
        db.add(FinancialPlan(assessment_id=assessment.id, result=result))
        db.commit()
    return result


@router.post("/recommend-scheme")
def recommend(data: SchemeRecommendationRequest):
    try:
        return recommend_scheme(data.project_cost, data.calculated_financing)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/assessment/{assessment_id}")
def get_assessment(
    assessment_id: int,
    db: Session = Depends(_db),
    current_user: dict | None = Depends(get_optional_user),
):
    assessment = (
        db.query(EntrepreneurAssessment)
        .filter(EntrepreneurAssessment.id == assessment_id)
        .first()
    )
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")
    if current_user and assessment.user_uid and assessment.user_uid != current_user["uid"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this assessment.",
        )

    latest_analysis = (
        db.query(BusinessAnalysis)
        .filter(BusinessAnalysis.assessment_id == assessment.id)
        .order_by(BusinessAnalysis.id.desc())
        .first()
    )
    latest_finance = (
        db.query(FinancialPlan)
        .filter(FinancialPlan.assessment_id == assessment.id)
        .order_by(FinancialPlan.id.desc())
        .first()
    )
    latest_scheme = (
        db.query(SchemeRecommendation)
        .filter(SchemeRecommendation.assessment_id == assessment.id)
        .order_by(SchemeRecommendation.id.desc())
        .first()
    )

    return {
        "assessment": {
            "id": assessment.id,
            "village": assessment.village,
            "block": assessment.block,
            "district": assessment.district,
            "state": assessment.state,
            "available_capital": assessment.available_capital,
            "business_category": assessment.business_category,
            "status": assessment.status,
            "created_at": (
                assessment.created_at.isoformat()
                if assessment.created_at
                else None
            ),
        },
        "analysis": latest_analysis.result if latest_analysis else None,
        "financial_plan": latest_finance.result if latest_finance else None,
        "scheme_recommendation": (
            latest_scheme.result if latest_scheme else None
        ),
    }