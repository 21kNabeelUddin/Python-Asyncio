import asyncio
import time

#unning Multiple Tasks "Create multiple async functions simulating I/O (e.g., download, email)",
# "Use asyncio.create_task() to schedule coroutines concurrently", "Use await asyncio.gather()
# to run multiple async functions in parallel", "Measure total execution time vs sequential version",
# "Handle exceptions in concurrent tasks with return_exceptions=True

async def download():
    await asyncio.sleep(2)

async def send_email():
    await asyncio.sleep(1)

async def run():
    # Sequential
    start = time.perf_counter()
    await download()
    await send_email()
    print(f"Sequential: {time.perf_counter() - start:.2f}s")

    # Concurrent
    start = time.perf_counter()
    await asyncio.gather(download(), send_email())
    print(f"Concurrent: {time.perf_counter() - start:.2f}s")

asyncio.run(run())
