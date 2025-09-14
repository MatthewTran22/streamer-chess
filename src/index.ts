import { AppServer, AppSession } from '@mentra/sdk';

const PACKAGE_NAME = process.env.PACKAGE_NAME ?? 'com.example.ttsapp';
const MENTRAOS_API_KEY = process.env.MENTRAOS_API_KEY ?? (() => { throw new Error('MENTRAOS_API_KEY is not set in .env file'); })();
const PORT = parseInt(process.env.PORT || '3000');
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

/**
 * TTS App with backend integration
 * Extends AppServer to provide button press handling and backend API calls
 */
class TTSApp extends AppServer {
  constructor() {
    super({
      packageName: PACKAGE_NAME,
      apiKey: MENTRAOS_API_KEY,
      port: PORT,
    });
  }

  /**
   * Call the backend API to send a message
   */
  private async callBackendAPI(userId: string, message: string): Promise<string> {
    console.log(`🔗 Calling backend API with message: "${message}" for user: ${userId}`);
    try {
      const response = await fetch(`${BACKEND_URL}/sendMsg`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          user_id: userId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(`📨 Backend API response:`, data);
      return data.message || 'No response from backend';
    } catch (error) {
      console.error('Backend API call failed:', error);
      throw error;
    }
  }

  /**
   * Handle new session creation and button press events
   */
  protected async onSession(session: AppSession, sessionId: string, userId: string): Promise<void> {
    console.log(`🎯 SESSION STARTED: ${sessionId} for user ${userId}`);
    this.logger.info(`🔊 TTS Session ${sessionId} started for ${userId}`);

    // Check speaker capabilities
    if (session.capabilities?.hasSpeaker && session.capabilities?.speaker) {
      const speaker = session.capabilities.speaker;
      console.log(`🔊 Speaker capabilities: ${speaker.count || 1} speakers, Private: ${speaker.isPrivate || false}`);
      this.logger.info(`Speakers: ${speaker.count || 1}, Private: ${speaker.isPrivate || false}`);
    }

    // Show welcome message
    console.log(`📱 Showing welcome message - TTS App Ready!`);
    session.layouts.showTextWall(`🔊 TTS App Ready!\n📡 Backend: ${BACKEND_URL}\nPress any button to call backend`, {
      durationMs: 5000
    });
    console.log(`✅ Session setup complete - waiting for button presses`);

    // Handle button press events - following the reference implementation pattern
    session.events.onButtonPress(async (button) => {
      console.log(`🔘 BUTTON PRESSED: ${button.buttonId} (${button.pressType})`);
      this.logger.info(`Button pressed: ${button.buttonId}, type: ${button.pressType}`);
      
      // Show loading message
      session.layouts.showTextWall('📡 Calling backend...', {
        durationMs: 1000
      });

      try {
        console.log(`🚀 Starting backend API call for button press`);
        // Call backend API to get message
        const backendMessage = await this.callBackendAPI(userId, "Button pressed!");
        console.log(`✅ Backend response received: ${backendMessage}`);
        this.logger.info(`Backend response: ${backendMessage}`);
        
        // Use TTS to speak the backend response
        console.log(`🎤 Starting TTS for message: "${backendMessage}"`);
        try {
          const ttsResult = await session.audio.speak(backendMessage);
          
          if (ttsResult.success) {
            console.log(`✅ TTS speech synthesis successful`);
            this.logger.info("TTS speech synthesis successful");
            // Also show text for visual confirmation
            session.layouts.showTextWall(`🔊 Speaking: "${backendMessage}"`, {
              durationMs: 2000
            });
          } else {
            console.log(`❌ TTS failed: ${ttsResult.error}`);
            this.logger.error(`❌ TTS failed: ${ttsResult.error}`);
            // Fallback to text display if TTS fails
            session.layouts.showTextWall(`${backendMessage} (TTS failed)`, {
              durationMs: 3000
            });
          }
        } catch (ttsError) {
          console.error(`💥 TTS exception: ${ttsError}`);
          this.logger.error(`TTS exception: ${ttsError}`);
          // Fallback to text display if TTS throws an error
          session.layouts.showTextWall(`${backendMessage} (TTS error)`, {
            durationMs: 3000
          });
        }
      } catch (error) {
        console.error(`💥 Exception during backend call: ${error}`);
        this.logger.error(`Exception during backend call: ${error}`);
        // Fallback to error message
        session.layouts.showTextWall('❌ Backend connection failed', {
          durationMs: 3000
        });
      }
    });
  }

  protected async onStop(sessionId: string, userId: string, reason: string): Promise<void> {
    this.logger.info(`Session stopped for user ${userId}, reason: ${reason}`);
  }
}

// Start the server
const app = new TTSApp();

app.start().catch(console.error);