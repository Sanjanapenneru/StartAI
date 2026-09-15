from gramai.context import EntrepreneurContext
from gramai.finance import calculate_financial_plan


def finance_agent(state: EntrepreneurContext) -> EntrepreneurContext:
    state["financial_plan"] = calculate_financial_plan(
        state["available_capital"]
    )
    state.setdefault("completed_agents", []).append("FINANCE_AGENT")
    return state