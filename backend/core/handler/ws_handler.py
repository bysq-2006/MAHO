class WSHandler():
    def __init__(self):
        pass

    async def handle_ws(self, websocket, Amadeus):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
