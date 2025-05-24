def bind_output_events(output_text, zoom_scale, zoom_mode_enabled):
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
