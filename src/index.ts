import { AppServer, AppSession } from '@mentra/sdk';
import { EventSource } from 'eventsource';

const PACKAGE_NAME = process.env.PACKAGE_NAME ?? 'com.example.ttsapp';
const MENTRAOS_API_KEY = process.env.MENTRAOS_API_KEY ?? (() => { throw new Error('MENTRAOS_API_KEY is not set in .env file'); })();
const PORT = parseInt(process.env.PORT || '3000');
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

/**
 * TTS App with backend integration
 * Extends AppServer to provide button press handling and backend SSE connection
 */
class TTSApp extends AppServer {
  private eventSource: EventSource | null = null;
  private isConnectedToSSE: boolean = false;

  constructor() {
    super({
      packageName: PACKAGE_NAME,
      apiKey: MENTRAOS_API_KEY,
      port: PORT,
    });
  }

  /**
   * Connect to backend SSE stream
   */
  private connectToSSE(session: AppSession): void {
    console.log(`🔗 Connecting to SSE stream: ${BACKEND_URL}/events`);
    
    try {
      this.eventSource = new EventSource(`${BACKEND_URL}/events`);
      this.isConnectedToSSE = true;

      this.eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log(`📨 SSE message received:`, data);
          
          // Speak the chess move via TTS
          this.handleChessMove(session, data.message);
        } catch (error) {
          console.error('Error parsing SSE data:', error);
        }
      };

      this.eventSource.onerror = (error) => {
        console.error('SSE connection error:', error);
        this.isConnectedToSSE = false;
        session.layouts.showTextWall('❌ SSE connection lost', { durationMs: 3000 });
      };

      this.eventSource.onopen = () => {
        console.log('✅ SSE connection opened');
        this.isConnectedToSSE = true;
        session.layouts.showTextWall('📡 Connected to chess stream', { durationMs: 2000 });
      };

    } catch (error) {
      console.error('Failed to create SSE connection:', error);
      this.isConnectedToSSE = false;
      session.layouts.showTextWall('❌ SSE connection failed', { durationMs: 3000 });
    }
  }

  /**
   * Handle incoming chess moves via TTS
   */
  private async handleChessMove(session: AppSession, message: string): Promise<void> {
    console.log(`🎤 Processing chess move: "${message}"`);
    
    try {
      const ttsResult = await session.audio.speak(message);
      
      if (ttsResult.success) {
        console.log(`✅ TTS speech synthesis successful for: "${message}"`);
        session.layouts.showTextWall(`🔊 ${message}`, { durationMs: 3000 });
      } else {
        console.log(`❌ TTS failed: ${ttsResult.error}`);
        session.layouts.showTextWall(`${message} (TTS failed)`, { durationMs: 3000 });
      }
    } catch (ttsError) {
      console.error(`💥 TTS exception: ${ttsError}`);
      session.layouts.showTextWall(`${message} (TTS error)`, { durationMs: 3000 });
    }
  }

  /**
   * Disconnect from SSE stream
   */
  private disconnectSSE(): void {
    if (this.eventSource) {
      console.log('🔌 Disconnecting from SSE stream');
      this.eventSource.close();
      this.eventSource = null;
      this.isConnectedToSSE = false;
    }
  }

  /**
   * Handle new session creation and SSE connection
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

    // Connect to SSE stream
    this.connectToSSE(session);

    // Show welcome message
    console.log(`📱 Showing welcome message - Chess TTS App Ready!`);
    session.layouts.showTextWall(`♟️ Chess TTS App Ready!\n📡 SSE: ${BACKEND_URL}/events\n🎧 Listening for chess moves...`, {
      durationMs: 5000
    });
    console.log(`✅ Session setup complete - SSE stream active`);

    // Handle button press events for manual trigger
    session.events.onButtonPress(async (button) => {
      console.log(`🔘 BUTTON PRESSED: ${button.buttonId} (${button.pressType})`);
      this.logger.info(`Button pressed: ${button.buttonId}, type: ${button.pressType}`);
      
      if (this.isConnectedToSSE) {
        session.layouts.showTextWall('♟️ SSE stream active\nChess moves will be spoken automatically', {
          durationMs: 3000
        });
      } else {
        session.layouts.showTextWall('❌ SSE not connected\nTrying to reconnect...', {
          durationMs: 2000
        });
        this.connectToSSE(session);
      }
    });
  }

  protected async onStop(sessionId: string, userId: string, reason: string): Promise<void> {
    console.log(`🛑 SESSION STOPPED: ${sessionId} for user ${userId}, reason: ${reason}`);
    this.logger.info(`Session stopped for user ${userId}, reason: ${reason}`);
    
    // Clean up SSE connection
    this.disconnectSSE();
  }
}

// Start the server
const app = new TTSApp();

app.start().catch(console.error);