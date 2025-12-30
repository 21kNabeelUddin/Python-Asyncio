import asyncio
import random

semaphore = asyncio.Semaphore(2)
startup_event = asyncio.Event()


async def initializer():
    print("[Initializer] Starting setup...")
    await asyncio.sleep(2)
    print("[Initializer] Setup complete")
    startup_event.set()


async def worker(name):

    print(f"[{name}] Waiting for initializer")
    await startup_event.wait()

    async with semaphore:
        try:
            work_time = random.uniform(1, 5)
            print(f"[{name}] Started (expected {work_time:.2f}s)")

            await asyncio.wait_for(
                asyncio.sleep(work_time),
                timeout=3
            )

            print(f"[{name}] Completed successfully")

        except asyncio.TimeoutError:
            print(f"[{name}] Timed out")

        except asyncio.CancelledError:
            print(f"[{name}] Cancelled")
            raise


async def main():
    init_task = asyncio.create_task(initializer())

    workers = [
        asyncio.create_task(worker(f"Worker-{i}"))
        for i in range(1, 6)
    ]
    all_tasks = [init_task] + workers

    try:
        await asyncio.wait_for(
            asyncio.gather(*all_tasks),
            timeout=8
        )
    except asyncio.TimeoutError:
        print("[Main] Global timeout reached, cancelling remaining tasks")
        for task in workers:
            task.cancel()

        await asyncio.gather(*workers, return_exceptions=True)


# Start the event loop
asyncio.run(main())
