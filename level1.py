import asyncio

#Write a simple coroutine (e.g., async def say_hello())", "Use asyncio.run() to execute your first coroutine

async def say_hello():
    print("initializing coroutine")
    await asyncio.sleep(1)
    print("completed coroutine")


asyncio.run(say_hello())