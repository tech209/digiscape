from scapy.all import IP, TCP, UDP, Ether

def parse_packet(packet):
    """Parses a raw packet and extracts useful metadata."""
    parsed_data = {}

    # Extract Ethernet layer data if present
    if packet.haslayer(Ether):
        parsed_data["src_mac"] = packet[Ether].src
        parsed_data["dst_mac"] = packet[Ether].dst

    # Extract IP layer data if present
    if packet.haslayer(IP):
        parsed_data["src_ip"] = packet[IP].src
        parsed_data["dst_ip"] = packet[IP].dst
        parsed_data["packet_length"] = packet[IP].len

    # Extract Transport Layer (TCP/UDP) if present
    if packet.haslayer(TCP):
        parsed_data["protocol"] = "TCP"
        parsed_data["src_port"] = packet[TCP].sport
        parsed_data["dst_port"] = packet[TCP].dport
        parsed_data["flags"] = packet[TCP].flags

    elif packet.haslayer(UDP):
        parsed_data["protocol"] = "UDP"
        parsed_data["src_port"] = packet[UDP].sport
        parsed_data["dst_port"] = packet[UDP].dport

    return parsed_data
