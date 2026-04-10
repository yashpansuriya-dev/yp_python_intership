import asyncio
from apify import Actor

# -------------------------------------------------------------------

async def main():
    async with Actor:
        print("hello from apify actor")

# -------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())