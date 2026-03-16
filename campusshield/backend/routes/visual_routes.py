# backend/routes/visual_routes.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class VisualRequest(BaseModel):
    url: str

@router.post("/analyze-visual")
async def analyze_visual(request: VisualRequest):
    return {
        "visual_similarity": None,
        "detected_brand":    None,
        "heatmap_url":       None,
        "risk":              None,
        "available":         False,
        "reason":            "Visual analysis coming soon"
    }