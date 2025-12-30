import asyncio
import websockets

connected_clients = set()
message_queue = asyncio.Queue()


async def register(websocket):
    connected_clients.add(websocket)
    print(f"[Server] Client connected ({len(connected_clients)})")


async def unregister(websocket):
    connected_clients.remove(websocket)
    print(f"[Server] Client disconnected ({len(connected_clients)})")


async def producer(websocket):
    """
    Receives messages from a client and pushes them to the queue.
    """
    async for message in websocket:
        await message_queue.put(message)


async def broadcaster():
    """
    Broadcasts messages from queue to all connected clients.
    """
    while True:
        message = await message_queue.get()

        for client in connected_clients.copy():
            try:
                await client.send(message)
            except:
                connected_clients.remove(client)

        message_queue.task_done()


async def handler(websocket):
    await register(websocket)

    producer_task = asyncio.create_task(producer(websocket))

    try:
        await producer_task
    finally:
        await unregister(websocket)


async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("[Server] Running on ws://localhost:8765")

    broadcaster_task = asyncio.create_task(broadcaster())

    await server.wait_closed()
    broadcaster_task.cancel()


asyncio.run(main())
