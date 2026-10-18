import html
import os

from .app_ref import get_app
from .thumbnail import create_fixed_thumbnail

CHANNEL_URL = "https://t.me/SKR_updates"


async def upload_file(user_id, path, title):
    app = get_app()
    safe_title = html.escape(str(title or os.path.basename(path)))
    caption = (
        f"🎬 {safe_title}\n\n"
        f'⚜️ Powered By : <a href="{CHANNEL_URL}">@SKR_updates</a>'
    )
    thumb_path = create_fixed_thumbnail(os.path.dirname(path) or ".")

    await app.send_document(
        user_id,
        path,
        caption=caption,
        parse_mode="html",
        thumb=thumb_path,
    )
