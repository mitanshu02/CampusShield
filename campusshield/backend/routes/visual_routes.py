# backend/routes/visual_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from analyzers.visual_detector import analyze_visual
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
_executor = ThreadPoolExecutor(max_workers=2)


class VisualRequest(BaseModel):
    url: str

@router.post("/analyze-visual")
async def analyze_visual_endpoint(request: VisualRequest):
    url = request.url.strip()
    if not url.startswith("http://") and \
       not url.startswith("https://"):
        url = "https://" + url

    loop   = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        _executor,
        analyze_visual,
        url
    )
    return result