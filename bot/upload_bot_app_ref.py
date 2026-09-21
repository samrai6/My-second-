_APP = None

def set_app(app):
    global _APP
    _APP = app

def get_app():
    if _APP is None:
        raise RuntimeError("Telegram app is not initialized")
    return _APP
