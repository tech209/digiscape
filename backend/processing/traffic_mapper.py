import time
import random
from capture.traffic_sniffer import capture_packet

def process_packet():
    """Processes a captured packet into density, latency, and adjustment values."""
    packet_data = capture_packet()

    # Simulate latency (real latency measurement can be added later)
    latency = random.uniform(0.01, 0.2)

    # Density is inversely proportional to latency (avoiding division by zero)
    density = 1 / max(latency, 0.001)

    # Adjustment value to determine emergent balancing
    adjustment = (density - latency) * 0.05

    return {
        "density": density,
        "latency": latency,
        "adjustment": adjustment
    }
