import cv2
import time
from ascii_engine import process_frame_diff, reset_ascii_state

from default_settings import DEFAULTS

def capture_loop(input_type, source, get_width, get_density, is_grayscale, update_output, stop_event, mirror=False):
    cap = cv2.VideoCapture(0 if input_type == "Webcam" else source)
    reset_ascii_state()  # reset previous_ascii buffer
    last_time = time.time()

    while cap.isOpened() and not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break

        if input_type == "Webcam" and mirror:
            frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ascii_art = process_frame_diff(gray, get_width(), get_density())

        fps = 1.0 / (time.time() - last_time)
        update_output(ascii_art, fps)
        last_time = time.time()

        time.sleep(1 / DEFAULTS["fps_cap"])

    cap.release()
