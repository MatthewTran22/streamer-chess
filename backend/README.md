# Streamer Chess Backend API

A FastAPI backend server for the Streamer Chess MentraOS application.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **TTS Integration**: Endpoints for text-to-speech functionality
- **Game Management**: Basic chess game state management
- **Docker Support**: Containerized deployment with Docker Compose
- **Health Checks**: Built-in health monitoring
- **CORS Support**: Cross-origin resource sharing enabled

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the container**:
   ```bash
   docker-compose up --build
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

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

## Environment Variables

- `PORT`: Server port (default: 8000)
- `ENV`: Environment mode (development/production)

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
docker-compose logs -f backend
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

## Future Enhancements

- Database integration (PostgreSQL)
- Redis caching
- Real TTS service integration
- WebSocket support for real-time updates
- Authentication and user management
- Chess game logic implementation
