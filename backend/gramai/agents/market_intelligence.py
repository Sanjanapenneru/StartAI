from gramai.context import EntrepreneurContext
from gramai.market_data import find_demo_profile
from services.llm_service import run_structured_analysis


def market_intelligence_agent(state: EntrepreneurContext) -> EntrepreneurContext:
    profile = find_demo_profile(
        state["state"], state["district"], state["business_category"]
    )
    fallback = lambda: {
        "label": "Prototype Estimate",
        "demand": profile["demand"],
        "target_customers": profile["customers"],
        "market_reach": (
            "Approximately 5–10 km around the selected village/block; "
            "validate with local visits."
        ),
        "opportunity": profile["opportunity"],
        "local_factors": [
            "seasonality",
            "transport access",
            "supplier reliability",
            "nearby institutions",
        ],
        "pricing_guidance": (
            "Compare at least three local providers and start with a "
            "transparent, service-inclusive price."
        ),
        "market_risks": [
            "demand may vary by season",
            "prototype data is not official government data",
        ],
    }
    prompt = (
        "Return only JSON for a hyper-local business market estimate. "
        f"Inputs: village={state['village']}, block={state['block']}, "
        f"district={state['district']}, state={state['state']}, "
        f"category={state['business_category']}, capital={state['available_capital']}. "
        "Use cautious estimates, never claim official statistics, and include "
        "keys: label, demand, target_customers, market_reach, opportunity, "
        "local_factors, pricing_guidance, market_risks."
    )
    result, mode = run_structured_analysis(prompt, fallback)
    state["market_analysis"] = result
    state["ai_mode"] = mode
    state.setdefault("completed_agents", []).append("MARKET_INTELLIGENCE_AGENT")
    return state