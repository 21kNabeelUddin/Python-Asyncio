#5 — Advanced Patterns "Implement a producer-consumer model using asyncio.Queue()", "Use async context managers (async with)", "Use async generators (async for) for streaming data", "Handle graceful shutdown and cancel running tasks", "Combine async I/O with threading or multiprocessing",


import asyncio
import random
import time
from contextlib import asynccontextmanager
async def data_stream():
    """
    Async generator that simulates streaming data.
    """
    for i in range(1, 11):
        await asyncio.sleep(0.5)  # simulate incoming data
        yield f"item-{i}"


@asynccontextmanager
async def managed_resource():
    """
    Async context manager for resource acquisition and cleanup.
    """
    print("[Resource] Acquired")
    try:
        yield
    finally:
        print("[Resource] Released")


def cpu_bound_work(data):
    """
    Simulates CPU-heavy computation.
    """
    time.sleep(1)
    return data.upper()

async def producer(queue):
    async with managed_resource():
        async for item in data_stream():
            print(f"[Producer] Produced {item}")
            await queue.put(item)

    print("[Producer] Finished producing")

async def consumer(name, queue):
    try:
        while True:
            item = await queue.get()
            print(f"[{name}] Consuming {item}")

            # Offload CPU-bound work to thread
            result = await asyncio.to_thread(cpu_bound_work, item)

            print(f"[{name}] Processed {result}")
            queue.task_done()

    except asyncio.CancelledError:
        print(f"[{name}] Cancelled")
        raise


async def main():
    queue = asyncio.Queue(maxsize=5)

    producer_task = asyncio.create_task(producer(queue))

    consumers = [
        asyncio.create_task(consumer(f"Consumer-{i}", queue))
        for i in range(1, 3)
    ]

    try:
        # Wait for producer to finish
        await producer_task

        # Wait until all produced items are processed
        await queue.join()

    finally:
        print("[Main] Shutting down consumers")
        for c in consumers:
            c.cancel()

        await asyncio.gather(*consumers, return_exceptions=True)

        print("[Main] Shutdown complete")


asyncio.run(main())
