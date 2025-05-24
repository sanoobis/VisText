import tkinter as tk
from tkinter import ttk
import threading
from camera_handler import capture_loop
from config import GRAPHICS_LEVELS, ASCII_STYLE_PACKS
from ascii_engine import set_ascii_style
from export_tools import save_as_txt, save_as_png, save_as_html

def setup_ui(root):
    stop_event = threading.Event()

    # Shared Tk Variables
    zoom_scale = tk.IntVar(value=6)
    use_fit_to_window = tk.BooleanVar(value=False)
    zoom_mode_enabled = tk.BooleanVar(value=True)
    graphics_quality = tk.StringVar(value="Medium (char_density 2)")
    color_mode = tk.StringVar(value="none")
    style_var = tk.StringVar(value="Default")
    input_type_var = tk.StringVar(value="Webcam")
    file_path = tk.StringVar()
    fps_label_var = tk.StringVar(value="FPS: ")
    menu_visible = tk.BooleanVar(value=True)

    # Output text area
    text_frame = tk.Frame(root)
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

    # Drag and scroll
    output_text.bind("<ButtonPress-1>", lambda e: output_text.scan_mark(e.x, e.y))
    output_text.bind("<B1-Motion>", lambda e: output_text.scan_dragto(e.x, e.y, gain=1))
    output_text.bind("<MouseWheel>", lambda e: (
        zoom_scale.set(max(1, min(zoom_scale.get() + (1 if e.delta > 0 else -1), 100))),
        output_text.config(font=("Courier", zoom_scale.get()))
    ) if (e.state & 0x0004) and zoom_mode_enabled.get() else output_text.yview_scroll(-1 * (e.delta // 120), "units"))

    # Right Menu
    menu_frame = tk.Frame(root, bd=1, relief="groove", bg="#eeeeee")
    menu_frame.place(relx=1.0, rely=1.0, anchor="se")

    main_frame = tk.Frame(menu_frame, bg="#eeeeee")
    row = 0

    # Input type
    ttk.Label(main_frame, text="Input Type:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    ttk.Combobox(main_frame, textvariable=input_type_var, values=["Webcam", "Image", "Video"], width=20).grid(row=row, column=1)

    row += 1
    ttk.Label(main_frame, text="File Path:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    file_entry = ttk.Entry(main_frame, textvariable=file_path, width=30)
    file_entry.grid(row=row, column=1)

    row += 1
    ttk.Label(main_frame, text="ASCII Width:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    width_entry = ttk.Entry(main_frame)
    width_entry.insert(0, "100")
    width_entry.grid(row=row, column=1)

    row += 1
    tk.Checkbutton(main_frame, text="Fit to Window", variable=use_fit_to_window, bg="#eeeeee").grid(row=row, column=0, columnspan=2, sticky="w")

    row += 1
    tk.Scale(main_frame, from_=4, to=100, orient="horizontal", variable=zoom_scale).grid(row=row, column=0, columnspan=2, sticky="we")

    row += 1
    ttk.Label(main_frame, text="Color Mode:", background="#eeeeee").grid(row=row, column=0, sticky="e")
    ttk.Combobox(main_frame, textvariable=color_mode, values=["none", "grayscale", "ansi"], width=20).grid(row=row, column=1)

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

    # Run loop
    def get_width():
        if use_fit_to_window.get():
            pixel_width = output_text.winfo_width()
            return max(20, int(pixel_width / (zoom_scale.get() * 0.6)))
        return int(width_entry.get())

    def get_density():
        return GRAPHICS_LEVELS.get(graphics_quality.get(), 0.45)

    def update_output(ascii_art, fps):
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, ascii_art)
        fps_label_var.set(f"FPS: %.2f" % fps)

    def start():
        stop_event.clear()
        source = file_path.get()
        thread = threading.Thread(target=capture_loop, args=(
            input_type_var.get(), source,
            get_width, get_density,
            lambda: color_mode.get() == "grayscale",
            update_output,
            stop_event,
            True
        ))
        thread.daemon = True
        thread.start()

    def stop():
        stop_event.set()

    row += 1
    ttk.Button(main_frame, text="Start", command=start).grid(row=row, column=0)
    ttk.Button(main_frame, text="Stop", command=stop).grid(row=row, column=1)

    row += 1
    ttk.Label(main_frame, textvariable=fps_label_var, background="#eeeeee").grid(row=row, column=0, columnspan=2)

    row += 1
    ttk.Button(main_frame, text="Save as TXT", command=lambda: save_as_txt(output_text.get("1.0", tk.END))).grid(row=row, column=0)
    ttk.Button(main_frame, text="Save as PNG", command=lambda: save_as_png(output_text.get("1.0", tk.END))).grid(row=row, column=1)

    row += 1
    ttk.Button(main_frame, text="Save as HTML", command=lambda: save_as_html(output_text.get("1.0", tk.END))).grid(row=row, column=0, columnspan=2)

    main_frame.pack()
    tk.Checkbutton(menu_frame, text="Hide Menu", variable=menu_visible,
                   command=lambda: main_frame.pack_forget() if not menu_visible.get() else main_frame.pack(),
                   bg="#eeeeee").pack(pady=2)
