# Streamer Chess Backend API

A FastAPI backend server for the Streamer Chess MentraOS application.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **TTS Integration**: Endpoints for text-to-speech functionality
- **Game Management**: Basic chess game state management
- **Docker Support**: Containerized deployment with Docker Compose
- **Health Checks**: Built-in health monitoring
- **CORS Support**: Cross-origin resource sharing enabled
- **Video Streaming**: RTMP to RTSP streaming with MediaMTX integration
- **OpenCV Integration**: Real-time video processing and display

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the container**:
   ```bash
   docker-compose up --build
   ```

2. **Access the services**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health
   - **RTMP stream input**: `rtmp://127.0.0.1:1935/live/stream1` ← **Publish here**
   - **RTSP stream output**: `rtsp://127.0.0.1:8554/live/stream1` ← **View here**

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python main.py
   ```

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /api/tts` - Text-to-speech conversion
- `GET /api/game/state` - Get current game state
- `POST /api/game/create` - Create a new chess game
- `POST /api/simulate/button-press` - Simulate button press for testing

### Example Usage

**Health Check**:
```bash
curl http://localhost:8000/health
```

**TTS Request**:
```bash
curl -X POST "http://localhost:8000/api/tts" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello World!"}'
```

**Simulate Button Press**:
```bash
curl -X POST "http://localhost:8000/api/simulate/button-press"
```

## Video Streaming Setup

This project uses **MediaMTX** for clean RTMP→RTSP streaming conversion.

**✅ Simplified Architecture:**
```
Publisher (OBS/ffmpeg) → MediaMTX (1935 RTMP) → MediaMTX (8554 RTSP) → OpenCV Client
```

### Quick Streaming Test

1. **Start the services**:
   ```bash
   docker-compose up
   ```

2. **Push a test stream** (using ffmpeg):
   ```bash
   ffmpeg -re -stream_loop -1 -i input.mp4 \
     -c:v libx264 -preset veryfast -tune zerolatency -g 30 -pix_fmt yuv420p \
     -c:a aac -b:a 128k -ar 48000 \
     -f flv rtmp://127.0.0.1:1935/live/stream1
   ```

3. **View the stream** with OpenCV:
   ```bash
   python opencv_rtsp_client.py
   ```

### Stream URLs

- **RTMP Input** (for publishers): `rtmp://127.0.0.1:1935/live/stream1`
- **RTSP Output** (for consumers): `rtsp://127.0.0.1:8554/live/stream1`

### Using with OBS Studio

1. Open OBS Studio
2. Go to Settings → Stream
3. Set Service to "Custom..."
4. Set Server to: `rtmp://127.0.0.1:1935/live/stream1`
5. Leave Stream Key empty
6. Click "Start Streaming"

### OpenCV Client Usage

The included OpenCV client automatically connects to the RTSP stream:

```bash
# Use default RTSP URL
python opencv_rtsp_client.py

# Use custom RTSP URL
python opencv_rtsp_client.py rtsp://192.168.1.100:8554/live/stream1

# Force UDP transport (TCP is default)
python opencv_rtsp_client.py --tcp false
```

**Controls**:
- `q` - Quit
- `f` - Toggle fullscreen
- `r` - Reset window size
- `s` - Save screenshot

### MediaMTX Configuration

MediaMTX is configured via `mediamtx.yml`. Key settings:

- **RTMP**: Port 1935 (input from publishers)
- **RTSP**: Port 8554 (output for consumers)  
- **WebRTC**: Port 8889 (for web browsers)
- **Transport**: TCP/UDP protocols enabled
- **Authentication**: Disabled for development (can be enabled)

To customize MediaMTX settings, edit `mediamtx.yml` and restart:
```bash
docker-compose restart mediamtx
```

## Environment Variables

- `PORT`: Server port (default: 8000)
- `ENV`: Environment mode (development/production)
- `MEDIAMTX_RTSP_URL`: RTSP output URL for video analysis (default: `rtsp://mediamtx:8554/live/stream1`)

## Docker Commands

**Build the image**:
```bash
docker build -t streamer-chess-backend .
```

**Run the container**:
```bash
docker run -p 8000:8000 streamer-chess-backend
```

**View logs**:
```bash
# Backend logs
docker-compose logs -f backend

# MediaMTX logs
docker-compose logs -f mediamtx

# All logs
docker-compose logs -f
```

**Stop services**:
```bash
docker-compose down
```

## Development

The server includes:
- Hot reload in development mode
- Automatic API documentation at `/docs`
- CORS enabled for frontend integration
- Health checks for container monitoring

## Troubleshooting

### Streaming Issues

**No video in OpenCV client**:
1. Check if MediaMTX is running: `docker-compose ps`
2. Verify RTMP stream is being published to MediaMTX
3. Check MediaMTX logs: `docker-compose logs mediamtx`
4. Test with different transport: `python opencv_rtsp_client.py --tcp false`

**High latency**:
1. MediaMTX uses TCP by default for stability
2. For lower latency, try UDP: `python opencv_rtsp_client.py --tcp false`
3. Adjust buffer size in OpenCV client
4. Use hardware encoding in your RTMP publisher

**Connection refused**:
1. Ensure ports 1935 (RTMP) and 8554 (RTSP) are not blocked
2. Check if services are bound to correct interfaces
3. For external access, use your machine's IP instead of 127.0.0.1

### MediaMTX Standalone

To run MediaMTX without Docker:

```bash
# Download and run MediaMTX directly
wget https://github.com/bluenviron/mediamtx/releases/latest/download/mediamtx_darwin_amd64.tar.gz
tar -xvzf mediamtx_darwin_amd64.tar.gz
./mediamtx
```

## Future Enhancements

- Database integration (PostgreSQL)
- Redis caching
- Real TTS service integration
- WebSocket support for real-time updates
- Authentication and user management
- Chess game logic implementation
- Stream recording and playback
- Multi-stream support
- Stream authentication and authorization
