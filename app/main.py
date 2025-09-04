from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, educate, match, chat

app = FastAPI(
    title="PsyAI API",
    version="0.1.0",
    description="HTTP API for PsyAI: education (RAG), psychologist matching, and chat."
)

# TODO: lock this down to your domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ["http://localhost:5173", "https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(educate.router)
app.include_router(match.router)
app.include_router(chat.router)
