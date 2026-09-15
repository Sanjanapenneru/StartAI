import math
from typing import Any


MICRO_PROJECT_LIMIT = 140_000.0
MICRO_MAX_LOAN = 125_000.0
MICRO_INTEREST_RATE = 0.065
MICRO_TENURE_YEARS = 3
MICRO_MORATORIUM_MONTHS = 3

TERM_PROJECT_LIMIT = 5_000_000.0
TERM_MAX_LOAN = 4_500_000.0
TERM_INTEREST_RATE = 0.08
TERM_TENURE_YEARS = 7
TERM_MORATORIUM_MONTHS = 6


def _money(value: float) -> float:
    return round(float(value), 2)


def _annuity_payment(principal: float, periodic_rate: float, periods: int) -> float:
    if periods <= 0 or principal <= 0:
        return 0.0
    if periodic_rate == 0:
        return principal / periods
    factor = (1 + periodic_rate) ** periods
    return principal * periodic_rate * factor / (factor - 1)


def _quarterly_schedule(
    loan: float,
    annual_rate: float,
    tenure_years: int,
    moratorium_months: int,
) -> dict[str, Any]:
    total_quarters = tenure_years * 4
    moratorium_quarters = math.ceil(moratorium_months / 3)
    repayment_quarters = max(total_quarters - moratorium_quarters, 0)
    quarterly_rate = annual_rate / 4
    payment = _annuity_payment(loan, quarterly_rate, repayment_quarters)
    balance = loan
    schedule = []

    for installment in range(1, repayment_quarters + 1):
        interest = balance * quarterly_rate
        principal = min(payment - interest, balance)
        actual_payment = principal + interest
        balance = max(balance - principal, 0)
        schedule.append(
            {
                "installment": installment,
                "due_after_months": moratorium_months + installment * 3,
                "opening_balance": _money(balance + principal),
                "interest": _money(interest),
                "principal": _money(principal),
                "payment": _money(actual_payment),
                "closing_balance": _money(balance),
            }
        )

    monthly_emi = _annuity_payment(
        loan, annual_rate / 12, tenure_years * 12
    )
    return {
        "quarterly_installments": repayment_quarters,
        "moratorium_quarters": moratorium_quarters,
        "estimated_quarterly_payment": _money(payment),
        "illustrative_monthly_emi": _money(monthly_emi),
        "quarterly_schedule": schedule,
    }


def calculate_financial_plan(available_capital: float) -> dict[str, Any]:
    try:
        capital = float(available_capital)
    except (TypeError, ValueError) as exc:
        raise ValueError("Available capital must be a positive number.") from exc

    if not math.isfinite(capital) or capital <= 0:
        raise ValueError("Available capital must be greater than zero.")

    project_cost = capital / 0.10
    calculated_financing = project_cost * 0.90

    if project_cost <= MICRO_PROJECT_LIMIT:
        scheme = "Micro Finance Scheme"
        maximum_loan = MICRO_MAX_LOAN
        interest_rate = MICRO_INTEREST_RATE
        tenure_years = MICRO_TENURE_YEARS
        moratorium_months = MICRO_MORATORIUM_MONTHS
    elif project_cost <= TERM_PROJECT_LIMIT:
        scheme = "Term Loan"
        maximum_loan = TERM_MAX_LOAN
        interest_rate = TERM_INTEREST_RATE
        tenure_years = TERM_TENURE_YEARS
        moratorium_months = TERM_MORATORIUM_MONTHS
    else:
        return {
            "supported": False,
            "scheme": None,
            "project_cost": _money(project_cost),
            "beneficiary_contribution": _money(project_cost * 0.10),
            "calculated_financing": _money(calculated_financing),
            "requested_or_calculated_loan": _money(calculated_financing),
            "scheme_maximum_loan": 0.0,
            "supported_loan": 0.0,
            "loan_gap": _money(calculated_financing),
            "reason": "Project exceeds the supported scheme limit.",
            "interest_rate": None,
            "tenure_years": None,
            "moratorium_months": None,
            "repayment": None,
        }

    supported_loan = min(calculated_financing, maximum_loan)
    return {
        "supported": True,
        "scheme": scheme,
        "project_cost": _money(project_cost),
        "beneficiary_contribution": _money(project_cost * 0.10),
        "calculated_financing": _money(calculated_financing),
        "requested_or_calculated_loan": _money(calculated_financing),
        "scheme_maximum_loan": _money(maximum_loan),
        "supported_loan": _money(supported_loan),
        "loan_gap": _money(max(calculated_financing - maximum_loan, 0)),
        "reason": f"{scheme} selected from deterministic project-cost rules.",
        "interest_rate": interest_rate,
        "tenure_years": tenure_years,
        "moratorium_months": moratorium_months,
        "repayment": _quarterly_schedule(
            supported_loan, interest_rate, tenure_years, moratorium_months
        ),
    }


def recommend_scheme(
    project_cost: float, calculated_financing: float | None = None
) -> dict[str, Any]:
    try:
        cost = float(project_cost)
    except (TypeError, ValueError) as exc:
        raise ValueError("Project cost must be a positive number.") from exc

    if not math.isfinite(cost) or cost <= 0:
        raise ValueError("Project cost must be greater than zero.")

    result = calculate_financial_plan(cost * 0.10)
    if calculated_financing is not None:
        requested = _money(float(calculated_financing))
        result["requested_or_calculated_loan"] = requested
        if result["supported"]:
            result["supported_loan"] = _money(
                min(requested, result["scheme_maximum_loan"])
            )
    return result