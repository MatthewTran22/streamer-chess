# MentraOS TTS App

A MentraOS application that tells you what move to play based on the chess board position.

## Features

- **Button Press Detection**: Listens for hardware button presses on the MentraOS glasses
- **Backend API Integration**: Calls FastAPI backend `/sendMsg` endpoint when button is pressed
- **Text-to-Speech (TTS)**: Uses MentraOS SDK's `session.audio.speak()` to play backend response audio
- **Visual Feedback**: Shows loading and confirmation messages during API calls
- **Error Handling**: Falls back to text display if backend or TTS fails
- **Speaker Capabilities**: Checks and logs available speaker information
- **Voice Activity Monitoring**: Displays voice activity status on the dashboard

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
4. Press any hardware button on the glasses
5. The app will call the backend API and speak the response through the glasses speakers

## Technical Notes

- **Backend Integration**: Makes HTTP POST requests to `/sendMsg` endpoint with user_id and message
- **TTS Implementation**: Uses MentraOS SDK's `session.audio.speak()` method for actual text-to-speech functionality
- **Error Handling**: Includes fallback to text display if backend API or TTS fails
- **Button Events**: The app listens for `onButtonPress` events and responds to any button press regardless of button ID or press type
- **Speaker Detection**: The app checks for available speakers and logs their capabilities (count, private audio support)
- **Async Operations**: Button press handler is async to properly handle API calls and TTS operations

## Dependencies

- `@mentra/sdk`: MentraOS SDK for smart glasses development
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