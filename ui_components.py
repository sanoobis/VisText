import tkinter as tk
from tkinter import ttk, filedialog
import threading
from ascii_engine import process_frame
from camera_handler import capture_loop
from config import *

def setup_ui(root):
    stop_flag = tk.BooleanVar(value=False)

    # Main variables
    menu_visible = tk.BooleanVar(value=True)
    zoom_mode_enabled = tk.BooleanVar(value=True)
    use_fit_to_window = tk.BooleanVar(value=False)
    zoom_scale = tk.IntVar(value=6)
    color_mode = tk.StringVar(value="none")
    graphics_quality = tk.StringVar(value="Medium (char_density 2)")
    fps_label_var = tk.StringVar(value="FPS: ")
    input_type_var = tk.StringVar(value="Webcam")
    file_path = tk.StringVar()

    # Output frame setup
    text_container = tk.Frame(root)
    text_container.pack(fill="both", expand=True)
    text_frame = tk.Frame(text_container)
    text_frame.pack(fill="both", expand=True)

    x_scroll = tk.Scrollbar(text_frame, orient="horizontal")
    y_scroll = tk.Scrollbar(text_frame, orient="vertical")

    output_text = tk.Text(text_frame, wrap=tk.NONE, font=("Courier", zoom_scale.get()), bg="black", fg="white",
                          xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, cursor="arrow")
    x_scroll.config(command=output_text.xview)
    y_scroll.config(command=output_text.yview)

    x_scroll.pack(side="bottom", fill="x")
    y_scroll.pack(side="right", fill="y")
    output_text.pack(side="left", fill="both", expand=True)

    def on_drag_start(event):
        output_text.scan_mark(event.x, event.y)

    def on_drag_motion(event):
        output_text.scan_dragto(event.x, event.y, gain=1)

    def on_mouse_wheel(event):
        if (event.state & 0x0004) and zoom_mode_enabled.get():
            delta = 1 if event.delta > 0 else -1
            new_zoom = zoom_scale.get() + delta
            zoom_scale.set(max(1, min(new_zoom, 100)))
            output_text.config(font=("Courier", zoom_scale.get()))
        elif not (event.state & 0x0004):
            output_text.yview_scroll(-1 * (event.delta // 120), "units")

    output_text.bind("<ButtonPress-1>", on_drag_start)
    output_text.bind("<B1-Motion>", on_drag_motion)
    output_text.bind("<MouseWheel>", on_mouse_wheel)

    # Menu setup
    menu_frame = tk.Frame(root, bd=1, relief="groove", bg="#eeeeee")
    menu_frame.place(relx=1.0, rely=1.0, anchor="se")
    main_frame = tk.Frame(menu_frame, bg="#eeeeee")

    def get_width():
        if use_fit_to_window.get():
            try:
                pixel_width = output_text.winfo_width()
                font_px = zoom_scale.get() * 0.6
                return max(20, int(pixel_width / font_px))
            except:
                return int(width_entry.get())
        return int(width_entry.get())

    def get_density():
        return GRAPHICS_LEVELS.get(graphics_quality.get(), 0.45)

    def update_output(ascii_art, fps):
        current_y = output_text.yview()
        current_x = output_text.xview()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, ascii_art)
        output_text.yview_moveto(current_y[0])
        output_text.xview_moveto(current_x[0])
        fps_label_var.set(f"FPS: {fps:.2f}")

    def browse_file():
        path = filedialog.askopenfilename()
        if path:
            file_path.set(path)

    def update_ui_visibility(*args):
        is_webcam = input_type_var.get() == "Webcam"
        file_path_entry.grid_remove() if is_webcam else file_path_entry.grid()
        browse_button.grid_remove() if is_webcam else browse_button.grid()

    def start_visualization():
        width = int(width_entry.get())
        input_type = input_type_var.get()
        source = file_path.get()

        if input_type == "Image":
            import cv2
            frame = cv2.imread(source)
            ascii_art = process_frame(frame, get_width(), get_density())
            update_output(ascii_art, 0.0)
        else:
            thread = threading.Thread(
                target=capture_loop,
                args=(input_type, source, get_width, get_density, lambda: color_mode.get() == "grayscale", update_output, True)
            )
            thread.daemon = True
            thread.start()

    def stop_visualization():
        nonlocal stop_flag
        stop_flag.set(True)

    input_type_var.trace_add("write", update_ui_visibility)

    row = 0
    tk.Label(main_frame, text="Input Type:", bg="#eeeeee").grid(row=row, column=0, sticky="e")
    ttk.Combobox(main_frame, textvariable=input_type_var, values=["Webcam", "Image", "Video"], width=20).grid(row=row, column=1)

    row += 1
    tk.Label(main_frame, text="File Path:", bg="#eeeeee").grid(row=row, column=0, sticky="e")
    file_path_entry = tk.Entry(main_frame, textvariable=file_path, width=30)
    file_path_entry.grid(row=row, column=1)
    browse_button = tk.Button(main_frame, text="Browse", command=browse_file)
    browse_button.grid(row=row, column=2)

    row += 1
    tk.Label(main_frame, text="ASCII Width:", bg="#eeeeee").grid(row=row, column=0, sticky="e")
    width_entry = tk.Entry(main_frame)
    width_entry.insert(0, "100")
    width_entry.grid(row=row, column=1)

    row += 1
    tk.Checkbutton(main_frame, text="Fit to Window", variable=use_fit_to_window, bg="#eeeeee").grid(row=row, column=0, columnspan=3, sticky="w")

    row += 1
    tk.Scale(main_frame, from_=4, to=100, orient="horizontal", variable=zoom_scale).grid(row=row, column=0, columnspan=3, sticky="we")

    row += 1
    tk.Label(main_frame, text="Color Mode:", bg="#eeeeee").grid(row=row, column=0, sticky="e")
    ttk.Combobox(main_frame, textvariable=color_mode, values=["none", "grayscale", "ansi"], width=20).grid(row=row, column=1)
    tk.Label(main_frame, text="(grayscale = GUI only, ansi = terminal only)", bg="#eeeeee").grid(row=row, column=2, sticky="w")

    row += 1
    tk.Checkbutton(main_frame, text="Enable Zoom Mode (Mouse Wheel)", variable=zoom_mode_enabled, bg="#eeeeee").grid(row=row, column=0, columnspan=3, sticky="w")

    row += 1
    tk.Label(main_frame, text="Graphics Quality (char_density):", bg="#eeeeee").grid(row=row, column=0, sticky="e")
    ttk.Combobox(main_frame, textvariable=graphics_quality, values=list(GRAPHICS_LEVELS.keys()), width=30).grid(row=row, column=1, columnspan=2)

    row += 1
    tk.Button(main_frame, text="Start", command=start_visualization).grid(row=row, column=0, columnspan=2)
    tk.Button(main_frame, text="Stop", command=stop_visualization).grid(row=row, column=2)

    row += 1
    tk.Label(main_frame, textvariable=fps_label_var, bg="#eeeeee").grid(row=row, column=0, columnspan=3)

    main_frame.pack()

    tk.Checkbutton(menu_frame, text="Hide Menu", variable=menu_visible,
                   command=lambda: main_frame.pack_forget() if not menu_visible.get() else main_frame.pack(),
                   bg="#eeeeee").pack(pady=2)

    update_ui_visibility()
