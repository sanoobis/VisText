import tkinter as tk
from tkinter import ttk

def build_output_area(parent, zoom_scale):
    frame = tk.Frame(parent)
    x_scroll = tk.Scrollbar(frame, orient="horizontal")
    y_scroll = tk.Scrollbar(frame, orient="vertical")

    text = tk.Text(frame, wrap=tk.NONE, font=("Courier", zoom_scale.get()), bg="black", fg="white",
                   xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, cursor="arrow")

    x_scroll.config(command=text.xview)
    y_scroll.config(command=text.yview)

    x_scroll.pack(side="bottom", fill="x")
    y_scroll.pack(side="right", fill="y")
    text.pack(side="left", fill="both", expand=True)

    frame.pack(fill="both", expand=True)
    return text

def build_settings_menu(parent):
    menu_frame = tk.Frame(parent, bd=1, relief="groove", bg="#eeeeee")
    menu_frame.place(relx=1.0, rely=1.0, anchor="se")
    return menu_frame

def build_main_controls(menu_frame):
    main_frame = tk.Frame(menu_frame, bg="#eeeeee")
    main_frame.pack()
    return main_frame
