from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text

from services.database import Base


class StartupWorkspace(Base):
    __tablename__ = "startup_workspaces"

    id = Column(Integer, primary_key=True, index=True)
    startup_name = Column(String)
    mode = Column(String)
    domain = Column(String)
    startup_description = Column(String)
    startup_state = Column(JSON)
    user_uid = Column(String, index=True)
    user_email = Column(String)
    user_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class EntrepreneurAssessment(Base):
    __tablename__ = "entrepreneur_assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_uid = Column(String, index=True, nullable=True)
    village = Column(String, nullable=False)
    block = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)
    available_capital = Column(Float, nullable=False)
    business_category = Column(String, nullable=False)
    experience = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    preferred_business_size = Column(String, nullable=True)
    status = Column(String, default="created", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BusinessAnalysis(Base):
    __tablename__ = "business_analyses"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(
        Integer, ForeignKey("entrepreneur_assessments.id"), nullable=False, index=True
    )
    result = Column(JSON, nullable=False)
    mode = Column(String, nullable=False, default="demo")
    created_at = Column(DateTime, default=datetime.utcnow)


class FinancialPlan(Base):
    __tablename__ = "financial_plans"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(
        Integer, ForeignKey("entrepreneur_assessments.id"), nullable=False, index=True
    )
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SchemeRecommendation(Base):
    __tablename__ = "scheme_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(
        Integer, ForeignKey("entrepreneur_assessments.id"), nullable=False, index=True
    )
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)