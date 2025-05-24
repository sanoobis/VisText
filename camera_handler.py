import cv2
import time
from ascii_engine import (
    frame_to_ascii,
    frame_to_ascii_color,
    process_frame_diff,
    reset_ascii_state,
    resize_frame
)
from default_settings import DEFAULTS
from config import GRAPHICS_LEVELS

def capture_loop(input_type, source, get_width, get_density, is_grayscale, update_output, stop_event, mirror=False):
    cap = cv2.VideoCapture(0 if input_type == "Webcam" else source)
    reset_ascii_state()
    last_time = time.time()

    color_mode = DEFAULTS["color_mode"]
    char_density = get_density()

    while cap.isOpened() and not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        if input_type == "Webcam" and mirror:
            frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if color_mode == "rgb":
            resized_gray = resize_frame(gray, get_width(), char_density)
            resized_color = resize_frame(frame, get_width(), char_density)
            ascii_rows = frame_to_ascii_color(resized_gray, resized_color)
            fps = 1.0 / (time.time() - last_time)
            update_output(ascii_rows, fps, is_rgb=True)

        elif color_mode == "grayscale":
            ascii_text = process_frame_diff(gray, get_width(), char_density)
            fps = 1.0 / (time.time() - last_time)
            if ascii_text:
                update_output(ascii_text, fps, is_rgb=False)

        else:  # fallback for "none" or "ansi"
            resized = resize_frame(gray, get_width(), char_density)
            ascii_text = "\n".join(frame_to_ascii(resized))
            fps = 1.0 / (time.time() - last_time)
            update_output(ascii_text, fps, is_rgb=False)

        last_time = time.time()
        time.sleep(1 / DEFAULTS["fps_cap"])

    cap.release()
