import asyncio
import os
import shutil

from .config import ENABLE_COMPRESSION, COMPRESS_HEIGHT, COMPRESS_CRF

SEM = asyncio.Semaphore(1)

async def compress_file(input_path, workdir):
    if not ENABLE_COMPRESSION:
        return input_path

    ext = os.path.splitext(input_path)[1].lower()
    if ext not in (".mp4", ".mkv", ".mov", ".webm"):
        return input_path

    output_path = os.path.join(workdir, "compressed.mp4")
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", input_path,
        "-vf", f"scale=-2:{COMPRESS_HEIGHT}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", str(COMPRESS_CRF),
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart",
        output_path,
    ]

    async with SEM:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()
        if proc.returncode != 0 or not os.path.exists(output_path):
            print("FFmpeg:", stderr.decode(errors="ignore")[-2000:])
            return input_path

    try:
        os.remove(input_path)
    except OSError:
        pass
    return output_path
