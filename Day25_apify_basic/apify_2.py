from apify import Actor

async def main():
    async with Actor:
        print("Hello from Apify!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())