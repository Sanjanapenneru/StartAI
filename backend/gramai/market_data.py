DEMO_MARKET_DATA = [
    {
        "state": "Andhra Pradesh",
        "district": "Krishna",
        "category": "Dairy",
        "demand": "High",
        "competition": "Medium",
        "customers": ["households", "tea shops", "local sweet shops"],
        "opportunity": "Reliable fresh milk delivery and value-added dairy products.",
    },
    {
        "state": "Andhra Pradesh",
        "district": "NTR",
        "category": "Tailoring",
        "demand": "Medium",
        "competition": "Medium",
        "customers": ["families", "students", "self-help groups"],
        "opportunity": "Alterations, school uniforms, and doorstep order collection.",
    },
    {
        "state": "Andhra Pradesh",
        "district": "Krishna",
        "category": "Food & Catering",
        "demand": "High",
        "competition": "Medium",
        "customers": ["offices", "events", "schools"],
        "opportunity": "Pre-order meal boxes and small-event catering.",
    },
    {
        "state": "Any",
        "district": "Any",
        "category": "Mobile Repair",
        "demand": "Medium",
        "competition": "High",
        "customers": ["students", "farmers", "households"],
        "opportunity": "Transparent pricing, pickup service, and accessory bundles.",
    },
]


def find_demo_profile(state: str, district: str, category: str) -> dict:
    category_lower = category.strip().lower()
    district_lower = district.strip().lower()
    state_lower = state.strip().lower()

    for profile in DEMO_MARKET_DATA:
        if profile["category"].lower() == category_lower and (
            profile["district"].lower() in {"any", district_lower}
            or profile["state"].lower() in {"any", state_lower}
        ):
            return profile

    for profile in DEMO_MARKET_DATA:
        if profile["category"].lower() == category_lower:
            return profile

    return {
        "state": state,
        "district": district,
        "category": category,
        "demand": "Medium",
        "competition": "Medium",
        "customers": ["nearby households", "local institutions"],
        "opportunity": (
            "Differentiate through dependable service, transparent pricing, "
            "and local delivery."
        ),
    }