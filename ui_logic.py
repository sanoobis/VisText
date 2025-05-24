from config import GRAPHICS_LEVELS

def get_width(output_text, zoom_scale, use_fit_to_window, fallback_width):
    if use_fit_to_window.get():
        pixel_width = output_text.winfo_width()
        return max(20, int(pixel_width / (zoom_scale.get() * 0.6)))
    return int(fallback_width.get())

def get_density(graphics_quality):
    return GRAPHICS_LEVELS.get(graphics_quality.get(), 0.45)

def update_output(output_text, fps_label_var, ascii_data, fps, is_rgb=False):
    output_text.configure(state="normal")
    output_text.delete("1.0", "end")

    if is_rgb:
        # ascii_data = List[List[(char, hex_color)]]
        for row_index, row in enumerate(ascii_data):
            for col_index, (char, hex_color) in enumerate(row):
                tag_name = f"fg_{hex_color}"
                if tag_name not in output_text.tag_names():
                    output_text.tag_config(tag_name, foreground=hex_color)
                index = f"{row_index + 1}.{col_index}"
                output_text.insert(index, char, tag_name)
            output_text.insert("end", "\n")
    else:
        output_text.insert("1.0", ascii_data)

    output_text.configure(state="disabled")
    fps_label_var.set(f"FPS: {fps:.2f}")
