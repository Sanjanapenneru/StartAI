from gramai.agents.business_feasibility import business_feasibility_agent
from gramai.agents.competitor_opportunity import competitor_opportunity_agent
from gramai.agents.finance import finance_agent
from gramai.agents.market_intelligence import market_intelligence_agent
from gramai.agents.scheme import scheme_recommendation_agent
from gramai.context import EntrepreneurContext


def _final_recommendation(state: EntrepreneurContext) -> EntrepreneurContext:
    feasibility = state["feasibility_analysis"]
    plan = state["financial_plan"]
    state["final_recommendation"] = {
        "headline": feasibility["recommendation"],
        "why_this_business": feasibility.get("strengths", [])[:5],
        "key_risks": (
            feasibility.get("risks", [])[:5]
            or feasibility.get("threats", [])[:5]
        ),
        "risk_reduction": [
            "validate demand with local customers",
            "compare supplier prices",
            "start with a small pilot",
            "track weekly cash flow",
            "confirm scheme documents with the channelizing agency",
        ],
        "next_steps": [
            "Validate local demand",
            "Compare supplier prices",
            "Finalize project cost",
            "Prepare required documents",
            "Approach the appropriate channelizing agency",
        ],
        "financial_note": plan["reason"],
    }
    state.setdefault("completed_agents", []).append("FINAL_RECOMMENDATION")
    return state


def build_workflow():
    try:
        from langgraph.graph import END, StateGraph

        graph = StateGraph(EntrepreneurContext)
        graph.add_node("market_intelligence", market_intelligence_agent)
        graph.add_node("business_feasibility", business_feasibility_agent)
        graph.add_node("competitor_opportunity", competitor_opportunity_agent)
        graph.add_node("finance", finance_agent)
        graph.add_node("scheme_recommendation", scheme_recommendation_agent)
        graph.add_node("final_recommendation", _final_recommendation)
        graph.set_entry_point("market_intelligence")
        graph.add_edge("market_intelligence", "business_feasibility")
        graph.add_edge("business_feasibility", "competitor_opportunity")
        graph.add_edge("competitor_opportunity", "finance")
        graph.add_edge("finance", "scheme_recommendation")
        graph.add_edge("scheme_recommendation", "final_recommendation")
        graph.add_edge("final_recommendation", END)
        return graph.compile()
    except ImportError:
        return _SequentialWorkflow()


class _SequentialWorkflow:
    def invoke(self, state: EntrepreneurContext) -> EntrepreneurContext:
        for node in (
            market_intelligence_agent,
            business_feasibility_agent,
            competitor_opportunity_agent,
            finance_agent,
            scheme_recommendation_agent,
            _final_recommendation,
        ):
            state = node(state)
        return state