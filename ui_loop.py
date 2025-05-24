import cv2
from ascii_engine import (
    frame_to_ascii_color,
    frame_to_ascii,
    resize_frame
)
from default_settings import DEFAULTS

def ui_render_loop(cap, input_type, get_width, get_density, color_mode, output_text, fps_label_var, stop_event, update_output):
    fps_cap = DEFAULTS["fps_cap"]
    last_time = 0

    while cap.isOpened() and not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1) if input_type == "Webcam" else frame
        color = color_mode()

        if color == "rgb":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized_gray = resize_frame(gray, new_width=get_width(), char_density=get_density())
            resized_color = resize_frame(frame, new_width=get_width(), char_density=get_density())
            ascii_rows = frame_to_ascii_color(resized_gray, resized_color)
            fps = 1.0 / max((cv2.getTickCount() - last_time) / cv2.getTickFrequency(), 1e-5)
            last_time = cv2.getTickCount()
            update_output(ascii_rows, fps, is_rgb=True)

        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = resize_frame(gray, new_width=get_width(), char_density=get_density())
            ascii_lines = frame_to_ascii(resized)
            ascii_text = "\n".join(ascii_lines)
            fps = 1.0 / max((cv2.getTickCount() - last_time) / cv2.getTickFrequency(), 1e-5)
            last_time = cv2.getTickCount()
            update_output(ascii_text, fps, is_rgb=False)

        cv2.waitKey(int(1000 / fps_cap))

    cap.release()
