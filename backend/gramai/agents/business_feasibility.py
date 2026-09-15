from gramai.context import EntrepreneurContext
from services.llm_service import run_structured_analysis


def business_feasibility_agent(state: EntrepreneurContext) -> EntrepreneurContext:
    market = state["market_analysis"]
    competition = state.get("competition_analysis", {})
    demand_points = {"High": 34, "Medium": 24, "Low": 12}
    competition_points = {"Low": 26, "Medium": 20, "High": 12}
    score = min(
        100,
        max(
            0,
            demand_points.get(str(market.get("demand")), 22)
            + competition_points.get(
                str(competition.get("competition_level")), 18
            )
            + 24,
        ),
    )
    fallback = lambda: {
        "score": score,
        "demand": market.get("demand", "Medium"),
        "competition": competition.get("competition_level", "Medium"),
        "opportunity": "Good" if score >= 65 else "Needs validation",
        "risk_level": (
            "Low" if score >= 78 else "Medium" if score >= 55 else "High"
        ),
        "strengths": [
            "local focus",
            "clear customer segments",
            "manageable prototype scope",
        ],
        "weaknesses": [
            "limited verified market data",
            "supplier and demand assumptions need validation",
        ],
        "opportunities": competition.get("underserved_niches", []),
        "threats": [
            "price pressure",
            "seasonal demand",
            "established local providers",
        ],
        "risks": market.get("market_risks", []),
        "recommendation": (
            "Highly promising"
            if score >= 78
            else (
                "Recommended with moderate risk"
                if score >= 55
                else "Consider an alternative business"
            )
        ),
    }
    prompt = (
        "Return only JSON for a business feasibility assessment. "
        f"Market: {market}. Competition: {competition}. "
        "Do not change financial values or scheme eligibility. Include score, "
        "demand, competition, opportunity, risk_level, strengths, weaknesses, "
        "opportunities, threats, risks, recommendation."
    )
    result, mode = run_structured_analysis(prompt, fallback)
    result["score"] = max(0, min(100, int(result.get("score", score))))
    state["feasibility_analysis"] = result
    if state.get("ai_mode") != "gemini":
        state["ai_mode"] = mode
    state.setdefault("completed_agents", []).append("BUSINESS_FEASIBILITY_AGENT")
    return state