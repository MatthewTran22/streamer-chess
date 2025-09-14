from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import asyncio
import json

# Initialize FastAPI app
app = FastAPI(
    title="Streamer Chess Backend API",
    description="Backend API for the Streamer Chess MentraOS application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class MessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class MessageResponse(BaseModel):
    success: bool
    message: str
    response: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Streamer Chess Backend API is running"
    )

# Send message endpoint
@app.post("/sendMsg")
async def send_message(request: MessageRequest):
    """
    Send a message - stub implementation
    This endpoint would handle message processing and responses
    """
    try:
        # Stub implementation - just echo back the message
        return {"message": "Rook to B1"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Message processing failed: {str(e)}")

# Server-Sent Events endpoint
@app.get("/events")
async def stream_events():
    """
    Stream chess moves via Server-Sent Events
    Sends "Rook to B1" every 5 seconds
    """
    async def event_generator():
        while True:
            # Send the chess move
            data = {
                "message": "Rook to B1",
                "timestamp": asyncio.get_event_loop().time()
            }
            yield f"data: {json.dumps(data)}\n\n"
            
            # Wait 5 seconds before sending the next event
            await asyncio.sleep(5)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Streamer Chess Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "sendMsg": "/sendMsg",
            "events": "/events (SSE - streams chess moves every 5 seconds)"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENV") == "development" else False
    )
