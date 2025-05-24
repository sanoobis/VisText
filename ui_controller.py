import tkinter as tk
from tkinter import ttk
from config import GRAPHICS_LEVELS, ASCII_STYLE_PACKS
from ascii_engine import set_ascii_style
from export_tools import save_as_txt, save_as_png, save_as_html
from ui_state import init_state
from ui_layout import build_output_area, build_settings_menu, build_main_controls
from ui_bindings import bind_output_events
from ui_logic import get_width, get_density, update_output
from ui_runner import start_stream, stop_stream, capture_once
from default_settings import DEFAULTS
import threading

def setup_ui(root):
    init_state(root)
    from ui_state import zoom_scale, use_fit_to_window, zoom_mode_enabled, graphics_quality
    from ui_state import color_mode, style_var, input_type_var, file_path, fps_label_var, menu_visible

    stop_event = threading.Event()
    output_text = build_output_area(root, zoom_scale)
    menu_frame = build_settings_menu(root)
    main_frame = build_main_controls(menu_frame)

    bind_output_events(output_text, zoom_scale, zoom_mode_enabled)
    set_ascii_style(style_var.get())

    row = 0
    ttk.Label(main_frame, text="Input Type:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    input_box = ttk.Combobox(main_frame, textvariable=input_type_var, values=["Webcam", "Image", "Video"], width=20)
    input_box.grid(row=row, column=1)

    row += 1
    ttk.Label(main_frame, text="File Path:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    file_entry = ttk.Entry(main_frame, textvariable=file_path, width=30)
    file_entry.grid(row=row, column=1)

    row += 1
    ttk.Label(main_frame, text="ASCII Width:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    width_entry = ttk.Entry(main_frame)
    width_entry.insert(0, str(DEFAULTS["ascii_width"]))
    width_entry.grid(row=row, column=1)

    row += 1
    tk.Checkbutton(main_frame, text="Fit to Window", variable=use_fit_to_window, bg="#eeeeee").grid(row=row, column=0, columnspan=2, sticky="w")

    row += 1
    tk.Scale(main_frame, from_=4, to=100, orient="horizontal", variable=zoom_scale).grid(row=row, column=0, columnspan=2, sticky="we")

    row += 1
    ttk.Label(main_frame, text="Color Mode:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    ttk.Combobox(main_frame, textvariable=color_mode, values=["none", "grayscale", "ansi", "rgb"], width=20).grid(row=row, column=1)

    row += 1
    tk.Checkbutton(main_frame, text="Enable Zoom Mode", variable=zoom_mode_enabled, bg="#eeeeee").grid(row=row, column=0, columnspan=2, sticky="w")

    row += 1
    ttk.Label(main_frame, text="Graphics Quality:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    ttk.Combobox(main_frame, textvariable=graphics_quality, values=list(GRAPHICS_LEVELS.keys()), width=30).grid(row=row, column=1)

    row += 1
    ttk.Label(main_frame, text="ASCII Style:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    style_dropdown = ttk.Combobox(main_frame, textvariable=style_var, values=list(ASCII_STYLE_PACKS.keys()), width=20)
    style_dropdown.grid(row=row, column=1)
    style_var.trace_add("write", lambda *args: set_ascii_style(style_var.get()))

    # Actions
    def get_w(): return get_width(output_text, zoom_scale, use_fit_to_window, width_entry)
    def get_d(): return get_density(graphics_quality)
    def update_fn(art, fps, is_rgb): update_output(output_text, fps_label_var, art, fps, is_rgb)

    def on_start():
        start_stream(stop_event, file_path, input_type_var, get_w, get_d, color_mode, output_text, fps_label_var, update_fn)

    def on_stop():
        stop_stream(stop_event)

    def on_capture():
        capture_once(file_path, input_type_var, get_w, get_d, color_mode, output_text, fps_label_var, update_fn)

    row += 1
    start_btn = ttk.Button(main_frame, text="Start", command=on_start)
    capture_btn = ttk.Button(main_frame, text="Capture", command=on_capture)
    stop_btn = ttk.Button(main_frame, text="Stop", command=on_stop)

    start_btn.grid(row=row, column=0)
    capture_btn.grid(row=row, column=1)
    stop_btn.grid(row=row, column=2)

    def toggle_capture_visibility(*_):
        if input_type_var.get() == "Webcam":
            capture_btn.grid()
        else:
            capture_btn.grid_remove()

    input_type_var.trace_add("write", toggle_capture_visibility)
    toggle_capture_visibility()  # run once on load

    row += 1
    ttk.Label(main_frame, textvariable=fps_label_var, background="#eeeeee").grid(row=row, column=0, columnspan=3)

    row += 1
    ttk.Button(main_frame, text="Save as TXT", command=lambda: save_as_txt(output_text.get("1.0", tk.END))).grid(row=row, column=0)
    ttk.Button(main_frame, text="Save as PNG", command=lambda: save_as_png(output_text.get("1.0", tk.END))).grid(row=row, column=1)

    row += 1
    ttk.Button(main_frame, text="Save as HTML", command=lambda: save_as_html(output_text.get("1.0", tk.END))).grid(row=row, column=0, columnspan=2)

    tk.Checkbutton(menu_frame, text="Hide Menu", variable=menu_visible,
                   command=lambda: main_frame.pack_forget() if not menu_visible.get() else main_frame.pack(),
                   bg="#eeeeee").pack(pady=2)
