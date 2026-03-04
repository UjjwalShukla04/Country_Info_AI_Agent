from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from main import create_graph
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(title="Country Info AI Agent API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, specify frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LangGraph agent
agent = create_graph()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    error: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Country Info AI Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if not request.question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        initial_state = {"question": request.question, "messages": []}
        result = agent.invoke(initial_state)
        
        return ChatResponse(
            answer=result.get("answer", "No answer generated."),
            error=result.get("error")
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
