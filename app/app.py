from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import json
import websockets

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve WebSocket passthrough
@app.websocket("/ws")
async def websocket_endpoint(websocket: websockets.WebSocketServerProtocol):
    """Forwards WebSocket data from interfaceServer to frontend."""
    await websocket.accept()
    async with websockets.connect("ws://localhost:5000") as source_ws:
        while True:
            data = await source_ws.recv()
            await websocket.send(data)

@app.get("/")
async def root():
    return {"message": "digiScape App Server Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
