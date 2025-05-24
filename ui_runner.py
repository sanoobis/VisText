import threading
from camera_handler import capture_loop

def start_stream(stop_event, get_width, get_density, is_grayscale, update_output, source, input_type):
    stop_event.clear()
    thread = threading.Thread(target=capture_loop, args=(
        input_type, source,
        get_width, get_density,
        is_grayscale,
        update_output,
        stop_event,
        True
    ))
    thread.daemon = True
    thread.start()

def stop_stream(stop_event):
    stop_event.set()
