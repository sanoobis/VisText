import cv2
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import time

ASCII_CHARS = "@%#*+=-:. "
stop_flag = False

graphics_levels = {
    "Low (char_density 1)": 0.35,
    "Medium (char_density 2)": 0.45,
    "High (char_density 3)": 0.55,
    "Ultra (char_density 4)": 0.65
}

def resize_frame(frame, new_width, char_density):
    height, width = frame.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * char_density)
    return cv2.resize(frame, (new_width, new_height))

def gray_to_ascii(gray_frame, use_grayscale=False):
    ascii_image = ""
    for row in gray_frame:
        for pixel in row:
            char = ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256]
            ascii_image += char
        ascii_image += "\n"
    return ascii_image

def process_frame(frame, width, use_grayscale, char_density):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = resize_frame(gray, new_width=width, char_density=char_density)
    return gray_to_ascii(small, use_grayscale=use_grayscale)

def run_ascii_visualizer(source, width, input_type, text_widget):
    global stop_flag
    stop_flag = False
    last_time = time.time()

    def update_output(ascii_art, fps):
        current_y = text_widget.yview()
        current_x = text_widget.xview()
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, ascii_art)
        text_widget.yview_moveto(current_y[0])
        text_widget.xview_moveto(current_x[0])
        fps_label_var.set(f"FPS: {fps:.2f}")

    def get_width():
        if use_fit_to_window.get():
            try:
                pixel_width = text_widget.winfo_width()
                font_px = zoom_scale.get() * 0.6  # Approx char width
                return max(20, int(pixel_width / font_px))
            except:
                return width
        return width

    char_density = graphics_levels.get(graphics_quality.get(), 0.45)
    text_widget.config(font=("Courier", zoom_scale.get()))

    if input_type == "Image":
        frame = cv2.imread(source)
        ascii_art = process_frame(frame, get_width(), color_mode.get() == "grayscale", char_density)
        update_output(ascii_art, 0.0)
    else:
        cap = cv2.VideoCapture(0 if input_type == "Webcam" else source)
        while cap.isOpened() and not stop_flag:
            ret, frame = cap.read()
            if not ret:
                break
            if input_type == "Webcam":
                frame = cv2.flip(frame, 1)
            start_time = time.time()
            ascii_art = process_frame(frame, get_width(), color_mode.get() == "grayscale", char_density)
            fps = 1.0 / (start_time - last_time)
            update_output(ascii_art, fps)
            last_time = start_time
            time.sleep(1 / 30)
        cap.release()

def start_visualization():
    input_type = input_type_var.get()
    source = file_path.get()
    width = int(width_entry.get())
    thread = threading.Thread(target=run_ascii_visualizer, args=(source, width, input_type, output_text))
    thread.daemon = True
    thread.start()

def browse_file():
    path = filedialog.askopenfilename()
    if path:
        file_path.set(path)

def stop_visualization():
    global stop_flag
    stop_flag = True

# GUI Setup
root = tk.Tk()
root.title("ASCII Visualizer")

menu_visible = tk.BooleanVar(value=True)
zoom_mode_enabled = tk.BooleanVar(value=True)
use_fit_to_window = tk.BooleanVar(value=False)
zoom_scale = tk.IntVar(value=6)
color_mode = tk.StringVar(value="none")
graphics_quality = tk.StringVar(value="Medium (char_density 2)")
fps_label_var = tk.StringVar(value="FPS: ")
input_type_var = tk.StringVar(value="Webcam")
file_path = tk.StringVar()

# Output text area
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

# Mouse drag scroll
def on_drag_start(event):
    output_text.scan_mark(event.x, event.y)

def on_drag_motion(event):
    output_text.scan_dragto(event.x, event.y, gain=1)

output_text.bind("<ButtonPress-1>", on_drag_start)
output_text.bind("<B1-Motion>", on_drag_motion)

# Mouse wheel zoom
def on_mouse_wheel(event):
    if (event.state & 0x0004) and zoom_mode_enabled.get():
        delta = 1 if event.delta > 0 else -1
        new_zoom = zoom_scale.get() + delta
        zoom_scale.set(max(1, min(new_zoom, 100)))
        output_text.config(font=("Courier", zoom_scale.get()))
    elif not (event.state & 0x0004):
        output_text.yview_scroll(-1 * (event.delta // 120), "units")

output_text.bind("<MouseWheel>", on_mouse_wheel)

# Menu panel
menu_frame = tk.Frame(root, bd=1, relief="groove", bg="#eeeeee")
menu_frame.place(relx=1.0, rely=1.0, anchor="se")

main_frame = tk.Frame(menu_frame, bg="#eeeeee")

# Callback for webcam toggle UI changes
def update_ui_visibility(*args):
    is_webcam = input_type_var.get() == "Webcam"
    browse_widgets_state = tk.NORMAL if not is_webcam else tk.HIDDEN
    file_path_entry.grid_remove() if is_webcam else file_path_entry.grid()
    browse_button.grid_remove() if is_webcam else browse_button.grid()

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
ttk.Combobox(main_frame, textvariable=graphics_quality, values=list(graphics_levels.keys()), width=30).grid(row=row, column=1, columnspan=2)

row += 1
tk.Button(main_frame, text="Start", command=start_visualization).grid(row=row, column=0, columnspan=2)
tk.Button(main_frame, text="Stop", command=stop_visualization).grid(row=row, column=2)

row += 1
tk.Label(main_frame, textvariable=fps_label_var, bg="#eeeeee").grid(row=row, column=0, columnspan=3)

main_frame.pack()

menu_toggle = tk.Checkbutton(menu_frame, text="Hide Menu", variable=menu_visible,
                             command=lambda: main_frame.pack_forget() if not menu_visible.get() else main_frame.pack(),
                             bg="#eeeeee")
menu_toggle.pack(pady=2)

update_ui_visibility()
root.mainloop()
