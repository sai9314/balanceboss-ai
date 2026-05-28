import os
import vertexai
from vertexai.generative_models import GenerativeModel

_initialized = False

SYSTEM_PROMPT = """You are BalanceBoss, an AI financial analyst for small businesses.
You help owners understand their sales and expenses, spot discrepancies, and surface
actionable insights from their uploaded financial data. Be concise and specific."""


def _init():
    global _initialized
    if not _initialized:
        vertexai.init(
            project=os.environ["GOOGLE_CLOUD_PROJECT"],
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        )
        _initialized = True


def ask_agent(question: str, context: str) -> str:
    _init()
    model = GenerativeModel("gemini-1.5-pro")
    prompt = f"{SYSTEM_PROMPT}\n\nFinancial Context:\n{context}\n\nQuestion: {question}"
    response = model.generate_content(prompt)
    return response.text
