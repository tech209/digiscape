import time
from capture.traffic_sniffer import packet_queue

def process_packet():
    """Processes a captured packet from any available source."""
    try:
        packet_data = packet_queue.get(timeout=1)

        # Simulated latency based on timestamp
        latency = max(time.time() - packet_data["timestamp"], 0.001)

        # Density based on inverse latency
        density = 1 / latency

        # Adjustment factor for emergent behavior
        adjustment = (density - latency) * 0.05

        return {
            "density": density,
            "latency": latency,
            "adjustment": adjustment,
            "src_ip": packet_data["src_ip"],
            "dst_ip": packet_data["dst_ip"],
            "source": packet_data["source"]
        }
    except queue.Empty:
        return None
