import asyncio
import aiohttp
import aiofiles
import aiosqlite


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def process(content):
    await asyncio.sleep(0.2)  # simulate processing
    return content.upper()


async def write_to_file(filename, content):
    async with aiofiles.open(filename, "a") as f:
        await f.write(content + "\n")


async def save_to_db(content):
    async with aiosqlite.connect("data.db") as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS results (content TEXT)"
        )
        await db.execute(
            "INSERT INTO results (content) VALUES (?)",
            (content,)
        )
        await db.commit()


async def save(content):
    await write_to_file("output.txt", content)
    await save_to_db(content)


async def pipeline(url):
    raw = await download(url)
    processed = await process(raw)
    await save(processed)


async def main():
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]

    await asyncio.gather(
        *(pipeline(url) for url in urls)
    )


asyncio.run(main())
