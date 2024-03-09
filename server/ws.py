from typing import List

from fastapi import FastAPI, WebSocket

app = FastAPI()


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endp(websocket: WebSocket, client_id: str):
    print(f"client id: {client_id}")
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        print(data)
        await manager.broadcast(f"{client_id}: {data}")
