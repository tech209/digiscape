import time

def get_current_timestamp():
    """Returns the current timestamp in seconds."""
    return time.time()

def format_timestamp(timestamp):
    """Formats a given timestamp into a readable string."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
