import json
import os

LOG_FILE = "logs/network_history.json"

def log_packet(packet_data):
    """Logs packet data to a JSON file."""
    os.makedirs("logs", exist_ok=True)
    
    with open(LOG_FILE, "a") as log_file:
        json.dump(packet_data, log_file)
        log_file.write("\n")
