import os
from PIL import Image, ImageDraw, ImageFont

PURPLE = (139, 55, 255)
DARK_PURPLE = (54, 20, 95)
BLACK = (10, 10, 16)
WHITE = (248, 245, 255)


def create_fixed_thumbnail(workdir):
    """Create the fixed SKR-branded JPEG thumbnail used on every upload."""
    os.makedirs(workdir, exist_ok=True)
    path = os.path.join(workdir, "skr_fixed_thumbnail.jpg")

    image = Image.new("RGB", (320, 180), BLACK)
    draw = ImageDraw.Draw(image)

    # Purple side panel and subtle neon-style framing.
    draw.rectangle((0, 0, 13, 180), fill=PURPLE)
    draw.rounded_rectangle((25, 18, 300, 162), radius=18, fill=(19, 16, 29), outline=PURPLE, width=3)
    draw.rounded_rectangle((42, 34, 278, 117), radius=14, fill=DARK_PURPLE, outline=(170, 104, 255), width=1)

    def load_font(size, bold=True):
        candidates = (
            ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
            if bold else
            ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
        )
        for candidate in candidates:
            if os.path.exists(candidate):
                return ImageFont.truetype(candidate, size)
        return ImageFont.load_default()

    brand_font = load_font(47)
    channel_font = load_font(17)
    label_font = load_font(10)

    brand = "SKR"
    bounds = draw.textbbox((0, 0), brand, font=brand_font, stroke_width=0)
    brand_x = (320 - (bounds[2] - bounds[0])) // 2
    draw.text((brand_x, 42), brand, font=brand_font, fill=WHITE, stroke_width=1, stroke_fill=PURPLE)

    channel = "@SKR_updates"
    bounds = draw.textbbox((0, 0), channel, font=channel_font)
    channel_x = (320 - (bounds[2] - bounds[0])) // 2
    draw.text((channel_x, 128), channel, font=channel_font, fill=WHITE)

    draw.text((236, 147), "LEECH BOT", font=label_font, fill=(190, 150, 255))

    image.save(path, "JPEG", quality=88, optimize=True)
    return path
