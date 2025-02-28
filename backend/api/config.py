import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# WebSocket Configuration
WS_HOST = os.getenv("WS_HOST", "127.0.0.1")
WS_PORT = int(os.getenv("WS_PORT", 5000))

# Network Capture Settings
CAPTURE_METHOD = os.getenv("CAPTURE_METHOD", "both")
NETWORK_INTERFACE = os.getenv("NETWORK_INTERFACE", "en0")

# Deco Mesh API Configuration
DECO_API_URL = os.getenv("DECO_API_URL", "http://192.168.68.1/api")
DECO_AUTH = os.getenv("DECO_AUTH", "user:password")

# Debug Mode
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
