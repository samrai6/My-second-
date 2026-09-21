from pyrogram import Client, filters
from pyrogram.types import Message
from .config import API_ID, API_HASH, BOT_TOKEN
from .queue import add_url_job, add_media_job, queue_size, cancel_user_job
from .utils import human_bytes, memory_text

app = Client(
    "skr_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=4,
)

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text(
        "🎬 **SKR Bot**\n\n"
        "Send a public video URL to download it.\n"
        "Reply to a Telegram media with `/compress` to compress it.\n\n"
        "Commands: /help /status /cancel"
    )

@app.on_message(filters.command("help"))
async def help_cmd(_, m: Message):
    await m.reply_text(
        "📌 **Commands**\n"
        "`/status` — queue + RAM status\n"
        "`/cancel` — cancel your queued task\n"
        "`/compress` — reply to a video/document to compress it\n\n"
        "You can also send a supported public URL."
    )

@app.on_message(filters.command("status"))
async def status(_, m: Message):
    await m.reply_text(f"📊 Queue: `{queue_size()}`\n🧠 {memory_text()}")

@app.on_message(filters.command("cancel"))
async def cancel(_, m: Message):
    if cancel_user_job(m.from_user.id):
        await m.reply_text("❌ Your queued task was cancelled.")
    else:
        await m.reply_text("No queued task found for you.")

@app.on_message(filters.command("compress"))
async def compress_cmd(_, m: Message):
    if not m.reply_to_message or not (
        m.reply_to_message.video or m.reply_to_message.document
    ):
        await m.reply_text("Reply to a video/document with `/compress`.")
        return
    ok, text = await add_media_job(m.from_user.id, m.reply_to_message)
    await m.reply_text(text)

@app.on_message(filters.text & ~filters.command(["start","help","status","cancel","compress"]))
async def url_handler(_, m: Message):
    text = (m.text or "").strip()
    if not (text.startswith("http://") or text.startswith("https://")):
        return
    ok, reply = await add_url_job(m.from_user.id, text)
    await m.reply_text(reply)
