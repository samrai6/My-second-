import asyncio
import os
import re
from yt_dlp import YoutubeDL

async def download_url(url, workdir):
    loop = asyncio.get_running_loop()

    def run():
        opts = {
            "outtmpl": os.path.join(workdir, "%(title)s [%(id)s].%(ext)s"),
            "format": "bv*+ba/b",
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "restrictfilenames": True,
        }
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title") or "SKR Download"
            requested = ydl.prepare_filename(info)
            base = os.path.splitext(requested)[0]
            for ext in ("mp4", "mkv", "webm", "mov"):
                p = base + "." + ext
                if os.path.exists(p):
                    return p, title
            for name in os.listdir(workdir):
                p = os.path.join(workdir, name)
                if os.path.isfile(p):
                    return p, title
            return None, title

    return await loop.run_in_executor(None, run)

async def download_telegram_media(message, workdir):
    name = None
    if message.video:
        name = message.video.file_name
    elif message.document:
        name = message.document.file_name
    name = name or f"telegram_{message.id}.bin"
    path = os.path.join(workdir, name)
    downloaded = await message.download(file_name=path)
    return downloaded, os.path.splitext(name)[0]
