# backend/routes/url_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.url_analyzer import analyze_url

router = APIRouter()

# This defines what the request body must look like
class URLRequest(BaseModel):
    url: str

@router.post("/analyze-url")
def analyze_url_endpoint(body: URLRequest):
    """
    Receives a URL from the frontend and returns full risk analysis.
    
    Request body:  { "url": "https://fees-nitbhopal-edu.in/pay" }
    Response:      { final_score, risk_label, signals, ... }
    """
    return analyze_url(body.url)