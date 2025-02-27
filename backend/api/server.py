import asyncio
import json
import websockets
from processing.traffic_mapper import process_packet

async def packet_stream(websocket, path):
    """Continuously sends processed packet data to the frontend via WebSockets."""
    while True:
        packet_data = process_packet()
        await websocket.send(json.dumps(packet_data))
        await asyncio.sleep(0.1)  # Adjust speed based on data flow needs

start_server = websockets.serve(packet_stream, "0.0.0.0", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
