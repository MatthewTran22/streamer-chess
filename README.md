# MentraOS Chess TTS App

A MentraOS application that automatically announces chess moves via Server-Sent Events (SSE) and Text-to-Speech.

## Features

- **Server-Sent Events (SSE)**: Connects to backend SSE stream for real-time chess move updates
- **Automatic TTS**: Announces chess moves every 5 seconds through the glasses speakers
- **Text-to-Speech (TTS)**: Uses MentraOS SDK's `session.audio.speak()` for natural voice output
- **Visual Feedback**: Shows connection status and incoming chess moves on screen
- **Error Handling**: Falls back to text display if backend or TTS fails
- **Speaker Capabilities**: Checks and logs available speaker information
- **Connection Management**: Automatic reconnection and proper cleanup

## Setup

1. **Install Dependencies**:
   ```bash
   bun install
   ```

2. **Environment Configuration**:
   Create a `.env` file in the root directory:
   ```env
   PORT=3000
   PACKAGE_NAME=com.example.ttsapp
   MENTRAOS_API_KEY=your_api_key_from_console
   BACKEND_URL=your_url
   ```

3. **Run the App**:
   ```bash
   # Development mode with hot reload
   bun run dev
   
   # Or production mode
   bun run start
   ```

## Usage

1. Connect your MentraOS glasses
2. Launch the app
3. Start the backend server (see backend/README.md for instructions)
4. The app automatically connects to the SSE stream
5. Chess moves ("Rook to B1") are announced every 5 seconds via TTS
6. Press any hardware button to check connection status

## Technical Notes

- **SSE Integration**: Connects to backend `/events` endpoint using EventSource for real-time streaming
- **TTS Implementation**: Uses MentraOS SDK's `session.audio.speak()` method for actual text-to-speech functionality
- **Error Handling**: Includes fallback to text display if SSE connection or TTS fails
- **Connection Management**: Automatic reconnection attempts and proper cleanup on session end
- **Speaker Detection**: The app checks for available speakers and logs their capabilities (count, private audio support)
- **Async Operations**: SSE message handling and TTS operations are properly async

## Dependencies

- `@mentra/sdk`: MentraOS SDK for smart glasses development
- `eventsource`: Server-Sent Events client for Node.js/Bun
- `@types/eventsource`: TypeScript definitions for EventSource
- `typescript`: TypeScript support
- `@types/node`: Node.js type definitions

## Architecture

The app extends the `AppServer` class and implements the `onSession` method to:
1. Set up event listeners for button presses
2. Check device capabilities
3. Display welcome message
4. Handle cleanup when the session ends

## Future Enhancements

- Add support for different button types and press patterns
- Include voice command integration
- Add configuration options for custom messages
- Implement advanced TTS settings (voice selection, speed, pitch)
- Add multiple language support