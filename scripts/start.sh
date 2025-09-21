#!/bin/bash
# Start Grape Challenge Unified Application (Production Mode)

cd grape-challenge
PYTHONPATH=. python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload