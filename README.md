# Async WebSocket Chat System (Python asyncio)
##Overview

This project is a real-time chat / notification system built using Python’s asyncio framework and WebSockets.
It demonstrates advanced asynchronous programming concepts, including:

Concurrent task execution

Producer–consumer patterns

Graceful shutdown handling

Real-time message broadcasting

Non-blocking I/O

Client–server architecture using WebSockets

The system consists of:

A WebSocket server (server.py)

One or more WebSocket clients (client.py)

Multiple clients can connect to the server and exchange messages in real time.



## How the System Works (High-Level)

The server starts and listens on ws://localhost:8765

Clients connect using WebSockets

Each client can:

Send messages

Receive messages concurrently

Messages are:

Received by the server

Placed into a queue

Broadcast to all connected clients

All communication is fully asynchronous

Server Implementation (server.py)
Responsibilities

Accept client connections

Track connected clients

Receive messages from clients

Broadcast messages to all clients

Handle disconnects cleanly

## Key Concepts Used in the Server
1. WebSocket Connection Handling
async with websockets.serve(handler, "localhost", 8765):


Starts the WebSocket server

Registers an async handler for each client

Runs inside the asyncio event loop

2. Tracking Connected Clients
connected_clients = set()


Maintains a set of active WebSocket connections

Clients are added on connect and removed on disconnect

3. Producer–Consumer Pattern
message_queue = asyncio.Queue()


Clients act as producers

Broadcaster task acts as consumer

Decouples receiving messages from broadcasting them

4. Message Producer
async for message in websocket:
    await message_queue.put((message, websocket))


Listens for incoming messages from a client

Pushes messages into the queue

5. Message Broadcaster
async def broadcaster():
    while True:
        message, sender = await message_queue.get()
        for client in connected_clients:
            await client.send(message)


Continuously consumes messages

Broadcasts them to all connected clients

This enables real-time chat behavior

6. Graceful Disconnect Handling
except websockets.exceptions.ConnectionClosed:
    pass
finally:
    connected_clients.remove(websocket)


Ensures disconnected clients are cleaned up

Prevents resource leaks

Client Implementation (client.py)
Responsibilities

Connect to the server

Send user input asynchronously

Receive messages concurrently

Shut down cleanly on disconnect or Ctrl+C

Key Concepts Used in the Client
1. Concurrent Send and Receive

Two async tasks run at the same time:

send_task = asyncio.create_task(send())
receive_task = asyncio.create_task(receive())


send() waits for user input

receive() listens for server messages

2. Handling Blocking Input Safely
msg = await asyncio.to_thread(input, "")


input() is blocking

Offloaded to a thread to avoid freezing the event loop

3. Graceful Shutdown
done, pending = await asyncio.wait(
    {send_task, receive_task},
    return_when=asyncio.FIRST_COMPLETED
)


If one task exits, the other is cancelled

Prevents crashes and orphaned tasks

4. Connection Close Handling
except ConnectionClosed:
    print("[Server] Connection closed")


Prevents unhandled exceptions

Ensures clean exit

How to Run the Project
1. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

2. Install Dependencies
pip install websockets

3. Start the Server
python server.py


Expected output:

[Server] Running on ws://localhost:8765

4. Start One or More Clients
python client.py


Expected output:

[User] Connected
