import threading
import scapy.all as scapy
import requests
import queue
from api.config import NETWORK_INTERFACE, DECO_API_URL, DECO_AUTH, CAPTURE_METHOD
from capture.deco_api import query_deco_network, query_deco_traffic

# Shared queue to store captured packets & Deco data
packet_queue = queue.Queue()

def capture_from_interface():
    """Captures live network packets from the local interface."""
    while True:
        packet = scapy.sniff(count=1, iface=NETWORK_INTERFACE)[0]
        packet_data = {
            "size": len(packet),
            "timestamp": packet.time,
            "protocol": packet.proto,
            "src_ip": packet[scapy.IP].src if packet.haslayer(scapy.IP) else "Unknown",
            "dst_ip": packet[scapy.IP].dst if packet.haslayer(scapy.IP) else "Unknown",
            "source": "interface"
        }
        packet_queue.put(packet_data)

def capture_from_deco():
    """Fetches live network data from Deco Mesh API."""
    while True:
        network_data = query_deco_network()
        traffic_data = query_deco_traffic()

        for device in network_data.get("devices", []):
            packet_data = {
                "src_ip": device["ip"],
                "dst_ip": "Deco Gateway",
                "protocol": "Unknown",
                "size": device.get("bandwidth", 0),
                "timestamp": device.get("last_active", 0),
                "source": "deco"
            }
            packet_queue.put(packet_data)

def start_capture():
    """Starts capture threads for both network interface and Deco API."""
    if CAPTURE_METHOD in ["interface", "both"]:
        threading.Thread(target=capture_from_interface, daemon=True).start()
    if CAPTURE_METHOD in ["deco", "both"]:
        threading.Thread(target=capture_from_deco, daemon=True).start()

start_capture()
