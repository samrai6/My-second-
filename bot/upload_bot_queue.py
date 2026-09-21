import asyncio
import os
import shutil
from dataclasses import dataclass
from collections import deque

from .config import MAX_QUEUE, DOWNLOAD_DIR
from .downloader import download_url, download_telegram_media
from .compressor import compress_file
from .uploader import upload_file

@dataclass
class Job:
    user_id: int
    kind: str
    source: object
    message: object = None
    compress: bool = False

QUEUE = deque()
ACTIVE = None
LOCK = asyncio.Lock()

def queue_size():
    return len(QUEUE) + (1 if ACTIVE else 0)

async def add_url_job(user_id, url):
    if len(QUEUE) >= MAX_QUEUE:
        return False, "⛔ Queue full. Please try again later."
    QUEUE.append(Job(user_id, "url", url, compress=True))
    return True, f"✅ Added to queue. Position: `{len(QUEUE)}`"

async def add_media_job(user_id, message):
    if len(QUEUE) >= MAX_QUEUE:
        return False, "⛔ Queue full. Please try again later."
    QUEUE.append(Job(user_id, "telegram", message, message=message, compress=True))
    return True, f"✅ Added to queue. Position: `{len(QUEUE)}`"

def cancel_user_job(user_id):
    for job in list(QUEUE):
        if job.user_id == user_id:
            QUEUE.remove(job)
            return True
    return False

async def worker():
    global ACTIVE
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    while True:
        if not QUEUE:
            await asyncio.sleep(1)
            continue

        ACTIVE = QUEUE.popleft()
        job = ACTIVE
        workdir = os.path.join(DOWNLOAD_DIR, str(job.user_id))
        os.makedirs(workdir, exist_ok=True)

        try:
            if job.kind == "url":
                path, title = await download_url(job.source, workdir)
            else:
                path, title = await download_telegram_media(job.message, workdir)

            if not path:
                continue

            if job.compress:
                compressed = await compress_file(path, workdir)
                if compressed:
                    path = compressed

            await upload_file(job.user_id, path, title)
        except Exception as e:
            print("JOB ERROR:", repr(e))
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
            ACTIVE = None
            await asyncio.sleep(0.5)
