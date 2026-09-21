from aiohttp import web
from .config import PORT
from .app_ref import set_app

async def health(_):
    return web.json_response({"status": "ok", "service": "skr-bot"})

async def start_health_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
