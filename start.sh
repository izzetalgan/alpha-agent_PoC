#!/bin/bash

echo "======================================"
echo " INITIATING ALPHA AGENT SYSTEM "
echo "======================================"

# Activate the virtual environment
source venv/bin/activate

# 1. Start the FastAPI backend in the background (using the '&' symbol)
echo "[1/2] Booting up the LangGraph Engine (Port 8000)..."
uvicorn api:api --reload &

# 2. Wait 2 seconds to ensure the API is fully awake
sleep 2

# 3. Start the Frontend UI server on port 8080
echo "[2/2] Booting up the Glass Box UI (Port 8080)..."
echo "======================================"
echo " ALL SYSTEMS GO! Open your browser to: http://localhost:8080"
echo "======================================"
python3 -m http.server 8080