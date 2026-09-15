import json
import os
from typing import Any, Callable


def get_llm():
    """Create Gemini lazily so the backend supports Prototype Demo Mode."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        temperature=0.2,
        max_retries=1,
    )


def _response_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)


def run_structured_analysis(
    prompt: str,
    fallback: Callable[[], dict],
) -> tuple[dict, str]:
    """Return (structured result, mode), falling back safely on Gemini errors."""
    model = get_llm()
    if model is None:
        return fallback(), "demo"

    try:
        response = model.invoke(prompt)
        cleaned = _response_text(response.content).strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned), "gemini"
    except Exception:
        return fallback(), "demo"


class _LazyLegacyLLM:
    def invoke(self, prompt: str):
        model = get_llm()
        if model is None:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured; use GRAMAI Prototype Demo Mode."
            )
        return model.invoke(prompt)


# Kept for compatibility with the original StartAI agents.
llm = _LazyLegacyLLM()