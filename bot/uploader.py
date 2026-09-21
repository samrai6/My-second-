import os
from .app_ref import get_app

async def upload_file(user_id, path, title):
    app = get_app()
    caption = f"🎬 {title}\n\n⚡ Powered by SKR"
    size = os.path.getsize(path)

    if size <= 49 * 1024 * 1024:
        await app.send_document(user_id, path, caption=caption)
    else:
        # Pyrofork/MTProto can handle larger Telegram uploads when supported
        # by the connected Telegram client.
        await app.send_document(user_id, path, caption=caption)
