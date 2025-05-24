import threading
import cv2
from ascii_engine import (
    reset_ascii_state,
    frame_to_ascii_color,
    frame_to_ascii,
    resize_frame
)
from default_settings import DEFAULTS

def start_stream(
    stop_event, file_path, input_type_var,
    get_width, get_density, color_mode,
    output_text, fps_label_var, update_output
):
    stop_event.clear()
    reset_ascii_state()

    source = file_path.get()
    input_type = input_type_var.get()

    def get_frame():
        return cv2.VideoCapture(0) if input_type == "Webcam" else cv2.VideoCapture(source)

    cap = get_frame()

    from ui_loop import ui_render_loop
    thread = threading.Thread(target=ui_render_loop, args=(
        cap,
        input_type,
        get_width,
        get_density,
        lambda: color_mode.get(),
        output_text,
        fps_label_var,
        stop_event,
        update_output
    ))
    thread.daemon = True
    thread.start()

def stop_stream(stop_event):
    stop_event.set()

def capture_once(
    file_path, input_type_var,
    get_width, get_density, color_mode,
    output_text, fps_label_var, update_output
):
    reset_ascii_state()
    input_type = input_type_var.get()
    cap = cv2.VideoCapture(0 if input_type == "Webcam" else file_path.get())
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return

    width = get_width()
    density = get_density()
    mode = color_mode.get()

    if mode == "rgb":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ascii_rows = frame_to_ascii_color(
            resize_frame(gray, width, density),
            resize_frame(frame, width, density)
        )
        update_output(ascii_rows, 0.0, is_rgb=True)
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ascii_text = "\n".join(frame_to_ascii(resize_frame(gray, width, density)))
        update_output(ascii_text, 0.0, is_rgb=False)
