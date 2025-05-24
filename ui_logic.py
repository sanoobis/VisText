from config import GRAPHICS_LEVELS

def get_width(output_text, zoom_scale, use_fit_to_window, fallback_width):
    if use_fit_to_window.get():
        pixel_width = output_text.winfo_width()
        return max(20, int(pixel_width / (zoom_scale.get() * 0.6)))
    return int(fallback_width.get())

def get_density(graphics_quality):
    return GRAPHICS_LEVELS.get(graphics_quality.get(), 0.45)

def update_output(output_text, fps_label_var, ascii_art, fps):
    y = output_text.yview()
    x = output_text.xview()

    current = output_text.get("1.0", "end-1c")
    if current != ascii_art:
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", ascii_art)
        output_text.yview_moveto(y[0])
        output_text.xview_moveto(x[0])
        output_text.configure(state="disabled")

    fps_label_var.set(f"FPS: {fps:.2f}")

