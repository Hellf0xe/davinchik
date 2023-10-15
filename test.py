import asyncio

async def timer(delay: float):
    await asyncio.sleep(delay)
    print(f"1")
    await timer(1)

async def main():
    task = asyncio.create_task(timer(1))
    await task


if __name__ == "__main__":
    asyncio.run(main())