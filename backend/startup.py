#!/usr/bin/env python3
"""
Startup script for Streamer Chess Backend
Sets up environment and runs Docker Compose
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def get_mac_ip():
    """Get the Mac's LAN IP address"""
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(['ipconfig', 'getifaddr', 'en0'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        else:
            # For other systems, you might need different commands
            print("⚠️  Not on macOS - you'll need to set YOUR_MAC_IP manually")
            return "YOUR_MAC_IP"
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get IP address: {e}")
        return "YOUR_MAC_IP"

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🚀 {description}...")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    print("🎬 Streamer Chess Backend Startup")
    print("=" * 40)
    
    # Get Mac IP
    mac_ip = get_mac_ip()
    print(f"📍 Detected Mac IP: {mac_ip}")
    
    # Set environment variables
    env = os.environ.copy()
    env['YOUR_MAC_IP'] = mac_ip
    env['RTMP_PUBLISHER_URL'] = f"rtmp://{mac_ip}:1936/s/in"
    
    print(f"📡 Publisher should connect to: rtmp://{mac_ip}:1936/s/in")
    print(f"👀 Viewers should connect to: rtmp://127.0.0.1:1935/live/streamKey")
    print()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    print(f"📁 Working directory: {backend_dir}")
    
    # Make sure start.sh is executable locally (for debugging)
    start_sh_path = backend_dir / "start.sh"
    if start_sh_path.exists():
        print("🔧 Making start.sh executable...")
        subprocess.run(['chmod', '+x', 'start.sh'], check=True)
    
    # Run docker compose
    print("\n🐳 Starting Docker Compose...")
    docker_cmd = ['docker', 'compose', 'up']
    
    try:
        # Run docker compose in the foreground so you can see logs
        subprocess.run(docker_cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        subprocess.run(['docker', 'compose', 'down'], env=env)
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker Compose failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
