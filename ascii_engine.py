import cv2
from config import ASCII_STYLE_PACKS, DEFAULT_STYLE

active_style = DEFAULT_STYLE

def set_ascii_style(style_name):
    global active_style
    if style_name in ASCII_STYLE_PACKS:
        active_style = style_name

def resize_frame(frame, new_width, char_density):
    height, width = frame.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * char_density)
    return cv2.resize(frame, (new_width, new_height))

def gray_to_ascii(gray_frame):
    ascii_chars = ASCII_STYLE_PACKS.get(active_style, ASCII_STYLE_PACKS[DEFAULT_STYLE])
    ascii_image = ""
    for row in gray_frame:
        for pixel in row:
            char = ascii_chars[int(pixel) * len(ascii_chars) // 256]
            ascii_image += char
        ascii_image += "\n"
    return ascii_image

def process_frame(frame, width, char_density):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = resize_frame(gray, width, char_density)
    return gray_to_ascii(resized)
