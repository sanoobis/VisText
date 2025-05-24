import argparse
import cv2
from ascii_engine import frame_to_ascii, resize_frame, set_ascii_style
from export_tools import save_as_txt, save_as_html, save_as_png
from config import GRAPHICS_LEVELS
from default_settings import DEFAULTS

def convert_image_to_ascii(input_path, output_path, width, char_density, style, export_format, color_mode):
    # Load and convert image
    frame = cv2.imread(input_path)
    if frame is None:
        print("❌ Could not load image:", input_path)
        return

    set_ascii_style(style)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = resize_frame(gray, new_width=width, char_density=char_density)
    ascii_lines = frame_to_ascii(resized)
    ascii_art = "\n".join(ascii_lines)

    # Save
    if export_format == "txt":
        save_as_txt(ascii_art, output_path)
    elif export_format == "html":
        save_as_html(ascii_art, output_path, text_color="#0f0" if color_mode == "grayscale" else "#fff")
    elif export_format == "png":
        save_as_png(ascii_art, output_path)
    else:
        print("❌ Unknown export format:", export_format)

    print(f"✅ Saved {export_format.upper()} to:", output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ASCII Art Image Converter")
    parser.add_argument("-i", "--input", required=True, help="Path to image file")
    parser.add_argument("-o", "--output", required=True, help="Output file path (without extension)")
    parser.add_argument("--width", type=int, default=DEFAULTS["ascii_width"], help="ASCII width")
    parser.add_argument("--style", default=DEFAULTS["ascii_style"], choices=["Default", "Light", "Dense", "Emoji", "Block"], help="ASCII character style")
    parser.add_argument("--quality", default=DEFAULTS["graphics_quality"], choices=list(GRAPHICS_LEVELS.keys()), help="Graphics quality level")
    parser.add_argument("--color", default=DEFAULTS["color_mode"], choices=["none", "grayscale", "ansi"], help="Color mode")
    parser.add_argument("--export", default="txt", choices=["txt", "html", "png"], help="Export format")

    args = parser.parse_args()

    convert_image_to_ascii(
        input_path=args.input,
        output_path=f"{args.output}.{args.export}",
        width=args.width,
        char_density=GRAPHICS_LEVELS[args.quality],
        style=args.style,
        export_format=args.export,
        color_mode=args.color
    )
