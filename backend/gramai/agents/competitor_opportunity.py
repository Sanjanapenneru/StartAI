from gramai.context import EntrepreneurContext
from gramai.market_data import find_demo_profile


def competitor_opportunity_agent(state: EntrepreneurContext) -> EntrepreneurContext:
    profile = find_demo_profile(
        state["state"], state["district"], state["business_category"]
    )
    state["competition_analysis"] = {
        "label": "Prototype Estimate",
        "competition_level": profile["competition"],
        "competitor_categories": [
            f"existing {state['business_category'].lower()} operators",
            "informal local providers",
            "nearby retail/service alternatives",
        ],
        "underserved_niches": [profile["opportunity"]],
        "differentiation_opportunities": [
            "reliable opening hours",
            "clear pricing",
            "local delivery or pickup",
            "repeat-customer service",
        ],
        "customer_segments": profile["customers"],
    }
    state.setdefault("completed_agents", []).append(
        "COMPETITOR_OPPORTUNITY_AGENT"
    )
    return state