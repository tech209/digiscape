import asyncio
import json
import websockets
from backend.processing.traffic_mapper import process_packet
from api.config import WS_HOST, WS_PORT, DEBUG

async def packet_stream(websocket, path):
    """Continuously sends processed network data from both sources."""
    while True:
        packet_data = process_packet()
        if packet_data:
            await websocket.send(json.dumps(packet_data))
            if DEBUG:
                print(f"Sent: {packet_data}")  # Debugging log
        await asyncio.sleep(0.1)  # Adjust delay

async def start_server():
    """Starts the WebSocket server."""
    server = await websockets.serve(packet_stream, WS_HOST, WS_PORT)
    print(f"Interface Server Running at ws://{WS_HOST}:{WS_PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
