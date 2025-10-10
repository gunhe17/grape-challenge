# pip
import uvicorn
from fastapi import FastAPI
# local
from grapechallenge.config import get_app_env

app = FastAPI(title="Grape Challenge")


# #
# Endpoints

@app.get("/health")
async def health():
    return {"status": "ok"}


# #
# main

if __name__ == "__main__":
    uvicorn.run(
        **{
            "app": "server:app",
            "host": "0.0.0.0",
            "port": 8000,
        }
    )