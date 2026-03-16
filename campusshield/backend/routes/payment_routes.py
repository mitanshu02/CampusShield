# backend/routes/payment_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.payment_analyzer import run_payment_analyzer

router = APIRouter()

class PaymentRequest(BaseModel):
    url: str

@router.post("/analyze-payment")
async def analyze_payment(request: PaymentRequest):
    url = request.url.strip()
    if not url.startswith("http://") and \
       not url.startswith("https://"):
        url = "https://" + url
    result = await run_payment_analyzer(url)
    return result