import asyncio
import os

from .config import ENABLE_COMPRESSION, COMPRESS_HEIGHT, COMPRESS_CRF

SEM = asyncio.Semaphore(1)
SUPPORTED_VIDEO_EXTENSIONS = (".mp4", ".mkv", ".mov", ".webm")
CHANNEL_URL = "https://t.me/SKR_updates"


async def compress_file(input_path, workdir):
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in SUPPORTED_VIDEO_EXTENSIONS:
        return input_path

    title = os.path.splitext(os.path.basename(input_path))[0]
    if ENABLE_COMPRESSION:
        output_path = os.path.join(workdir, "compressed.mp4")
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", input_path,
            "-map", "0",
            "-vf", f"scale=-2:{COMPRESS_HEIGHT}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", str(COMPRESS_CRF),
            "-c:a", "aac", "-b:a", "96k",
            "-metadata", f"title={title}",
            "-metadata", "artist=SKR",
            "-metadata", f"comment=Powered by @SKR_updates ({CHANNEL_URL})",
            "-metadata", "copyright=@SKR_updates",
            "-movflags", "+faststart",
            output_path,
        ]
    else:
        # Preserve the original streams while writing fixed metadata.
        output_path = os.path.join(workdir, f"metadata_fixed{ext}")
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", input_path, "-map", "0", "-c", "copy",
            "-metadata", f"title={title}",
            "-metadata", "artist=SKR",
            "-metadata", f"comment=Powered by @SKR_updates ({CHANNEL_URL})",
            "-metadata", "copyright=@SKR_updates",
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
            print("FFmpeg metadata/compression error:", stderr.decode(errors="ignore")[-2000:])
            return input_path

    try:
        os.remove(input_path)
    except OSError:
        pass
    return output_path
