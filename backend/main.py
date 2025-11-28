from fastapi import FastAPI, WebSocket
from core.handler.ws_handler import WSHandler
from core.core import BaseAmadeus

app = FastAPI()
ws_handler = WSHandler()

if __name__ == "__main__":
    Amadeus = BaseAmadeus()

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await ws_handler.handle_ws(websocket, Amadeus)
