from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from graph import app

# 1. Initialize the FastAPI Server
api = FastAPI(title="Alpha Agent PoC API", description="The Glass Box Engine Backend")

# 2. Add CORS Middleware
# CRITICAL for the frontend: This allows a web browser UI
# to talk to our local Python server without security blockages.
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For PoC, we allow all origins.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define the Expected Input (JSON Payload)
class AnalysisRequest(BaseModel):
    ticker: str
    client_profile: str = "Balanced" # Default if not provided

# 4. Create the Execution Endpoint
@api.post("/analyze")
async def analyze_stock(request: AnalysisRequest):
    print(f"\n[API LOG] Request received for {request.ticker} | Profile: {request.client_profile}")
    
    try:
        # Prepare the payload for LangGraph
        initial_state = {
            "ticker": request.ticker.upper(),
            "client_profile": request.client_profile,
            "news_report": "",
            "fundamentals_report": "",
            "risk_report": "",
            "final_decision": ""
        }
        
        # Fire up the LangGraph engine!
        result = app.invoke(initial_state)
        
        # Return the resulting state as a JSON response to the web frontend
        return {
            "status": "success",
            "ticker": result["ticker"],
            "client_profile": result["client_profile"],
            "reports": {
                "news": result["news_report"],
                "fundamentals": result["fundamentals_report"],
                "risk": result["risk_report"]
            },
            "master_decision": result["final_decision"]
        }
        
    except Exception as e:
        print(f"[API ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint just to check if server is alive
@api.get("/")
async def health_check():
    return {"status": "Alpha Agent API is running! 🚀"}