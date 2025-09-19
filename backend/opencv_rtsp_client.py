#!/usr/bin/env python3
"""
Simple OpenCV RTSP Client
Connects to an RTSP stream and displays it in OpenCV window
Works with MediaMTX RTSP streams
"""

import cv2
import sys
import argparse
import time
import os

def main():
    parser = argparse.ArgumentParser(description='OpenCV RTSP Stream Client')
    parser.add_argument('stream_url', nargs='?', 
                       default='rtsp://127.0.0.1:8554/live/stream1',
                       help='RTSP stream URL (default: rtsp://127.0.0.1:8554/live/stream1)')
    parser.add_argument('--tcp', action='store_true', default=True,
                       help='Force RTSP over TCP for stability (default: True)')
    
    args = parser.parse_args()
    
    # Force RTSP over TCP for stability (recommended for MediaMTX)
    if args.tcp:
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    
    print("🎥 OpenCV RTSP Stream Client")
    print("=" * 40)
    print(f"📡 Connecting to: {args.stream_url}")
    print(f"🔧 RTSP Transport: {'TCP' if args.tcp else 'UDP'}")
    print()
    print("🎮 Controls:")
    print("  - Press 'q' to quit")
    print("  - Press 'f' to toggle fullscreen")
    print("  - Press 'r' to reset window size")
    print("  - Press 's' to save screenshot")
    print()
    
    print("⏳ Connecting to RTSP stream...")
    
    # Connect to RTSP stream
    cap = cv2.VideoCapture(args.stream_url, cv2.CAP_FFMPEG)
    
    if not cap.isOpened():
        print(f"❌ Could not connect to RTSP stream: {args.stream_url}")
        print("💡 Make sure:")
        print("   - MediaMTX server is running")
        print("   - RTMP stream is being published to MediaMTX")
        print("   - The stream path is correct")
        print("   - Network connectivity is available")
        print()
        print("🔧 Try these commands:")
        print("   docker run --rm -it --network=host -e MTX_PROTOCOLS=tcp,udp bluenviron/mediamtx:latest")
        print("   ffmpeg -re -stream_loop -1 -i input.mp4 -c:v libx264 -preset veryfast -tune zerolatency -g 30 -pix_fmt yuv420p -c:a aac -b:a 128k -ar 48000 -f flv rtmp://127.0.0.1:1935/live/stream1")
        sys.exit(1)
    
    # Set buffer size for low latency
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Get stream info
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate frame delay to match original FPS
    frame_delay = 1.0 / 10.0  # Default to 30 FPS if unknown
    
    print(f"✅ Connected successfully!")
    print(f"📺 Stream info: {width}x{height} @ {fps} FPS")
    print(f"⏱️  Frame delay: {frame_delay:.3f}s ({1/frame_delay:.1f} FPS)")
    
    # Create window
    window_name = "RTSP Stream Viewer"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)
    
    fullscreen = False
    frame_count = 0
    screenshot_count = 0
    last_frame_time = time.time()
    no_frame_count = 0
    last_display_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                no_frame_count += 1
                if no_frame_count > 30:  # After 30 failed attempts
                    print("⚠️  No new frames for a while, attempting to reconnect...")
                    # Try to reconnect to RTSP stream
                    cap.release()
                    time.sleep(2)
                    cap = cv2.VideoCapture(args.stream_url, cv2.CAP_FFMPEG)
                    if not cap.isOpened():
                        print("❌ Could not reconnect to RTSP stream")
                        break
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    print("✅ Reconnected to RTSP stream")
                    no_frame_count = 0
                
                # Small delay to prevent busy waiting
                time.sleep(0.033)  # ~30 FPS check rate
                continue
            
            # Reset no frame counter when we get a frame
            no_frame_count = 0
            current_time = time.time()
            
            # Check if enough time has passed since last display (frame rate control)
            time_since_last_display = current_time - last_display_time
            if time_since_last_display < frame_delay:
                # Not time to display this frame yet, sleep for remaining time
                sleep_time = frame_delay - time_since_last_display
                time.sleep(sleep_time)
                current_time = time.time()
            
            last_frame_time = current_time
            last_display_time = current_time
            frame_count += 1
            
            # Add frame counter and timestamp overlay
            cv2.putText(frame, f"Stream Frame: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Add timestamp and FPS info to show live updates
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            cv2.putText(frame, f"Time: {timestamp}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            cv2.putText(frame, f"Target FPS: {1/frame_delay:.1f}", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
            
            # Display frame
            cv2.imshow(window_name, frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("🛑 Quit requested by user")
                break
            elif key == ord('f'):
                fullscreen = not fullscreen
                if fullscreen:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    print("📺 Fullscreen enabled")
                else:
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    print("📺 Windowed mode")
            elif key == ord('r'):
                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(window_name, 1280, 720)
                fullscreen = False
                print("📺 Window reset")
            elif key == ord('s'):
                screenshot_count += 1
                filename = f"stream_screenshot_{screenshot_count:03d}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
            
            # Print status every 100 frames with timing info
            if frame_count % 100 == 0:
                current_time = time.time()
                time_since_last = current_time - last_frame_time if frame_count > 100 else 0
                print(f"📊 Processed {frame_count} frames | Last frame: {time_since_last:.2f}s ago")
                
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"💥 Error: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("🧹 Cleanup complete")

if __name__ == "__main__":
    main()
