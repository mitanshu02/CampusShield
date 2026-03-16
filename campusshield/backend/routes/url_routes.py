# backend/routes/url_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.url_analyzer import analyze_url
from services.ai_explainer_service import generate_explanation

router = APIRouter()

class URLRequest(BaseModel):
    url: str

@router.post("/analyze-url")
def analyze_url_endpoint(body: URLRequest):
    # Step 1 — run all 4 signal checks
    result = analyze_url(body.url)

    # Step 2 — pass signals to Gemini for plain-English explanation
    explanation = generate_explanation(result["signals"])

    # Step 3 — add 3 new fields to response, all existing fields unchanged
    result["explanation"]           = explanation.get("explanation")
    result["impersonation_statement"] = explanation.get("impersonation_statement")
    result["attack_type"]           = explanation.get("attack_type")

    return result