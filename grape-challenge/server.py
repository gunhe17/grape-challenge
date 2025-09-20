import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database.database_json import json_db
from .routers import auth_router, users_router, sessions_router, fruits_router, missions_router, web_router

app = FastAPI(title="Grape Challenge API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# Include routers
app.include_router(web_router)  # Web routes first (for root path)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(fruits_router)
app.include_router(missions_router)

@app.get("/api")
def read_root():
    return {"message": "Grape Challenge API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}