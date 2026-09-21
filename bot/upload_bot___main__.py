import asyncio
from . import app
from .health import start_health_server
from .queue import worker

async def main():
    await app.start()
    await start_health_server()
    asyncio.create_task(worker())
    print("SKR Bot started")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
