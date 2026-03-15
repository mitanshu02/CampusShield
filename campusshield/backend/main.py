# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.url_routes import router as url_router

app = FastAPI(title="CampusShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "CampusShield backend running"}