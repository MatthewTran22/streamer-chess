from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import asyncio
import json
import cv2

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

def check_rtmp_stream_access(rtmp_url: str) -> tuple[bool, str]:
    """
    Check if we can actually access the RTMP stream using OpenCV
    Returns (is_accessible: bool, error_message: str)
    """
    try:
        # Create VideoCapture object with RTMP URL using FFmpeg backend
        cap = cv2.VideoCapture(rtmp_url, cv2.CAP_FFMPEG)
        
        if cap.isOpened():
            # Try to read one frame to verify stream is actually working
            ret, frame = cap.read()
            cap.release()  # Always release resources
            
            if ret and frame is not None:
                print(f"✅ RTMP stream accessible: {rtmp_url}")
                return True, "RTMP stream accessible"
            else:
                error_msg = f"RTMP stream opened but no frames received: {rtmp_url}"
                print(f"❌ {error_msg}")
                return False, error_msg
        else:
            error_msg = f"Could not open RTMP stream: {rtmp_url}"
            print(f"❌ {error_msg}")
            return False, error_msg
            
    except Exception as e:
        error_msg = f"Error testing RTMP stream {rtmp_url}: {str(e)}"
        print(f"💥 {error_msg}")
        return False, error_msg

def validate_message_requirements() -> tuple[bool, str]:
    """
    Validate all requirements for sending a message
    Returns (should_send: bool, reason: str)
    
    Add new requirements here as needed:
    - RTMP stream accessibility
    - Other stream parameters
    - API keys
    - Database connectivity
    - etc.
    """
    # Check RTMP_URL environment variable
    rtmp_url = os.getenv("RTMP_URL", "rtmp://rtmp-server:1935/live/streamKey")
    if not rtmp_url:
        return False, "No RTMP_URL environment variable set"
    
    # Check RTMP stream accessibility
    is_accessible, error_msg = check_rtmp_stream_access(rtmp_url)
    if not is_accessible:
        return False, error_msg
    
    # TODO: Add more requirements here as needed
    # Example:
    # if not os.getenv("API_KEY"):
    #     return False, "No API_KEY environment variable set"
    # 
    # if not check_database_connection():
    #     return False, "Database not accessible"
    
    return True, "All requirements met"

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
    Sends "Rook to B1" every 5 seconds if RTMP_URL is set AND accessible
    Tests actual RTMP stream connectivity using OpenCV VideoCapture
    Otherwise logs "RTMP stream not accessible - Looks the same"
    """
    async def event_generator():
        while True:
            # Validate all requirements for sending a message
            should_send, reason = validate_message_requirements()
            
            if should_send:
                # All requirements met - send the chess move
                data = {
                    "message": "Rook to B1",
                    "timestamp": asyncio.get_event_loop().time(),
                }
                yield f"data: {json.dumps(data)}\n\n"
                print(f"📺 {reason} - Sending chess move: {data['message']}")
            else:
                # Requirements not met - log reason and don't send
                print(f"📺 {reason} - Looks the same")
            
            # Wait 5 seconds before the next iteration
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
            "events": "/events (SSE - streams chess moves every 5 seconds if RTMP_URL is set)"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENV") == "development" else False
    )
