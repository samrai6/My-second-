import html
import os

from .app_ref import get_app

CHANNEL_URL = "https://t.me/SKR_updates"

async def upload_file(user_id, path, title):
    app = get_app()
    safe_title = html.escape(str(title or os.path.basename(path)))
    caption = (
        f"🎬 {safe_title}\n\n"
        f'⚜️ Powered By : <a href="{CHANNEL_URL}">@SKR_updates</a>'
    )
    await app.send_document(
        user_id,
        path,
        caption=caption,
        parse_mode="html",
    )
