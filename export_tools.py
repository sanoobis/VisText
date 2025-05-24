from PIL import Image, ImageDraw, ImageFont
import html
import os

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

def save_as_txt(ascii_art, filename="output.txt"):
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ascii_art)

def save_as_html(ascii_art, filename="output.html", font_family="Courier New", font_size=12, bg_color="#000", text_color="#0f0"):
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        escaped = html.escape(ascii_art).replace(" ", "&nbsp;").replace("\n", "<br>")
        f.write(f"""
        <html><head><style>
        body {{ background: {bg_color}; color: {text_color}; font-family: '{font_family}'; font-size: {font_size}px; white-space: pre; }}
        </style></head><body>{escaped}</body></html>
        """)

def save_as_png(ascii_art, filename="output.png", font_size=12):
    from PIL import ImageFont
    lines = ascii_art.splitlines()
    font = ImageFont.load_default()
    width = max(len(line) for line in lines) * font_size // 2
    height = len(lines) * font_size

    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        draw.text((0, i * font_size), line, fill="lime", font=font)

    img.save(os.path.join(EXPORT_DIR, filename))
