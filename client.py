import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

SERVER_URI = "ws://localhost:8765"


async def client(username):
    async with websockets.connect(SERVER_URI) as websocket:
        print("[User] Connected")

        async def send():
            try:
                while True:
                    # Run blocking input in a thread
                    msg = await asyncio.to_thread(input, "")
                    await websocket.send(f"{username}: {msg}")
            except (asyncio.CancelledError, ConnectionClosed):
                pass

        async def receive():
            try:
                async for message in websocket:
                    print(message)
            except ConnectionClosed:
                print("[Server] Connection closed")

        send_task = asyncio.create_task(send())
        receive_task = asyncio.create_task(receive())

        done, pending = await asyncio.wait(
            {send_task, receive_task},
            return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel remaining task(s)
        for task in pending:
            task.cancel()

        await asyncio.gather(*pending, return_exceptions=True)


asyncio.run(client("User"))
