# SKR Telegram Bot

A Pyrofork-based Telegram bot deployed as a Docker web service on Render.

## Start command

The Docker image uses `start.sh`, which runs `python -u -m bot` and streams Python logs immediately. Keep `Dockerfile`, `start.sh`, and `bot/__main__.py` together at the repository root/package paths shown here.

## Required Render environment variables

Set these in **Render → Service → Environment**. Do not commit real values or `.env` files.

- `API_ID` — Telegram API ID from my.telegram.org
- `API_HASH` — Telegram API hash from my.telegram.org
- `BOT_TOKEN` — token for the bot created with BotFather
- `OWNER_ID` — owner Telegram user ID (optional for basic startup)
- `UPLOAD_CHAT_ID` — upload destination chat ID (needed by upload features)

Optional settings have defaults in `bot/config.py`, including `PORT`, `MAX_QUEUE`, `MAX_FILE_GB`, and compression options.

## Deploy on Render

1. Select this repository and the `main` branch.
2. Use the Docker runtime and root `Dockerfile`; do not configure a separate conflicting start command.
3. Set the required environment variables in Render.
4. Deploy the latest commit and wait for `Telegram connected as @...` and `SKR Bot started and ready to receive messages` in logs.
5. Open the bot in Telegram and send `/start`. Logs should show `Incoming message` and `Received /start`.

## If `/start` does not reply

- If the service exits before `Telegram connected`, inspect the first Python traceback and check the Render environment variables.
- If Telegram connects but no `Incoming message` appears, confirm the `BOT_TOKEN` belongs to the exact bot being tested and that no other deployment is running the same bot token. Redeploy the latest `main` commit.
- Never share the bot token in screenshots or chat. If it is exposed, revoke it through BotFather and set the replacement in Render.

## Health endpoint

The service exposes `/health` on Render's assigned port. It indicates that the web health server is responding; Telegram connectivity is separately confirmed by the startup logs.
