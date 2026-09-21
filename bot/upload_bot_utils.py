import psutil

def human_bytes(n):
    n = float(n)
    for unit in ("B","KB","MB","GB","TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def memory_text():
    m = psutil.virtual_memory()
    return f"RAM: `{m.percent:.1f}%` ({human_bytes(m.used)} / {human_bytes(m.total)})"
