import scapy.all as scapy

def capture_packet():
    """Captures a single network packet and returns its metadata."""
    packet = scapy.sniff(count=1, iface="en0")[0]  # Change 'en0' to your network interface
    return {
        "size": len(packet),
        "timestamp": packet.time
    }
