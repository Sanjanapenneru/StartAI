from gramai.context import EntrepreneurContext


def scheme_recommendation_agent(state: EntrepreneurContext) -> EntrepreneurContext:
    plan = state["financial_plan"]
    if not plan["supported"]:
        reason = (
            "No supported scheme is recommended because the project cost "
            "exceeds ₹50,00,000."
        )
    else:
        reason = (
            f"{plan['scheme']} recommended because the estimated project cost "
            f"is ₹{plan['project_cost']:,.0f}."
        )
        if plan["loan_gap"] > 0:
            reason += (
                f" The scheme supports up to ₹{plan['scheme_maximum_loan']:,.0f}; "
                "the calculated financing is higher."
            )
    state["scheme_recommendation"] = {
        "eligible_scheme": plan["scheme"],
        "maximum_supported_loan": plan["scheme_maximum_loan"],
        "interest_rate": plan["interest_rate"],
        "repayment_period_years": plan["tenure_years"],
        "moratorium_months": plan["moratorium_months"],
        "reason": reason,
        "deterministic": True,
    }
    state.setdefault("completed_agents", []).append(
        "SCHEME_RECOMMENDATION_AGENT"
    )
    return state