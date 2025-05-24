import cv2
import numpy as np
from config import ASCII_STYLE_PACKS, DEFAULT_STYLE
from default_settings import DEFAULTS

active_style = DEFAULT_STYLE
previous_gray = None

def set_ascii_style(style_name):
    global active_style
    if style_name in ASCII_STYLE_PACKS:
        active_style = style_name

def resize_frame(frame, new_width, char_density):
    height, width = frame.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * char_density)
    return cv2.resize(frame, (new_width, new_height))

def maybe_blur(frame):
    if DEFAULTS["smooth_enabled"]:
        radius = DEFAULTS.get("smooth_blur_radius", 3)
        return cv2.GaussianBlur(frame, (radius | 1, radius | 1), 0)
    return frame

def get_smooth_ascii_chars():
    if DEFAULTS["smooth_enabled"]:
        smooth_style = DEFAULTS.get("smooth_ascii_mode", "Dense")
        return ASCII_STYLE_PACKS.get(smooth_style, ASCII_STYLE_PACKS[DEFAULT_STYLE])
    return ASCII_STYLE_PACKS.get(active_style, ASCII_STYLE_PACKS[DEFAULT_STYLE])

def frame_to_ascii(gray_frame):
    ascii_chars = get_smooth_ascii_chars()
    return [
        ''.join(ascii_chars[int(px) * len(ascii_chars) // 256] for px in row)
        for row in gray_frame
    ]

def frame_to_ascii_color(gray_frame, color_frame):
    ascii_chars = get_smooth_ascii_chars()
    granularity = DEFAULTS["color_granularity"]
    output = []

    for y in range(gray_frame.shape[0]):
        line = []
        for x in range(gray_frame.shape[1]):
            gray = gray_frame[y, x]
            char = ascii_chars[int(gray) * len(ascii_chars) // 256]

            b, g, r = color_frame[y, x]
            r = (r // granularity) * granularity
            g = (g // granularity) * granularity
            b = (b // granularity) * granularity

            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            line.append((char, hex_color))
        output.append(line)
    return output

def process_frame_diff(current_gray, width, char_density,
                       diff_thresh=DEFAULTS["pixel_diff_threshold"],
                       update_percent=DEFAULTS["update_percent"]):
    global previous_gray

    blurred = maybe_blur(current_gray)
    resized_gray = resize_frame(blurred, width, char_density)
    h, w = resized_gray.shape

    if previous_gray is None or previous_gray.shape != resized_gray.shape:
        previous_gray = resized_gray.copy()
        return "\n".join(frame_to_ascii(resized_gray))

    diff = cv2.absdiff(resized_gray, previous_gray)
    changed_pixels = np.sum(diff > diff_thresh)
    total_pixels = h * w
    change_ratio = changed_pixels / total_pixels

    if change_ratio > update_percent:
        previous_gray = resized_gray.copy()
        return "\n".join(frame_to_ascii(resized_gray))
    else:
        return None

def reset_ascii_state():
    global previous_gray
    previous_gray = None
