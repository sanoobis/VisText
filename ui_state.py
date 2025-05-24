import tkinter as tk
from default_settings import DEFAULTS

def init_state(root):
    global zoom_scale, use_fit_to_window, zoom_mode_enabled, graphics_quality
    global color_mode, style_var, input_type_var, file_path, fps_label_var, menu_visible

    zoom_scale = tk.IntVar(master=root, value=DEFAULTS["zoom_scale"])
    use_fit_to_window = tk.BooleanVar(master=root, value=DEFAULTS["fit_to_window"])
    zoom_mode_enabled = tk.BooleanVar(master=root, value=True)
    graphics_quality = tk.StringVar(master=root, value=DEFAULTS["graphics_quality"])
    color_mode = tk.StringVar(master=root, value=DEFAULTS["color_mode"])
    style_var = tk.StringVar(master=root, value=DEFAULTS["ascii_style"])
    input_type_var = tk.StringVar(master=root, value=DEFAULTS["input_type"])
    file_path = tk.StringVar(master=root, value=DEFAULTS["file_path"])
    fps_label_var = tk.StringVar(master=root, value=DEFAULTS["fps_label"])
    menu_visible = tk.BooleanVar(master=root, value=True)
