import socket

def get_local_ip():
    """Returns the local machine's IP address."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def is_private_ip(ip):
    """Checks if an IP address is private."""
    private_ranges = [
        ("10.", "10.255.255.255"),
        ("172.16.", "172.31.255.255"),
        ("192.168.", "192.168.255.255"),
    ]
    return any(ip.startswith(start) for start, _ in private_ranges)
