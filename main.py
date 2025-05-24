from tkinter import Tk
from ui_controller import setup_ui

if __name__ == "__main__":
    root = Tk()
    root.title("ASCII Visualizer")

    # ✅ Cross-platform fullscreen handling
    try:
        root.state("zoomed")  # Windows
    except:
        try:
            root.attributes("-zoomed", True)  # Linux (older method)
        except:
            root.attributes("-fullscreen", True)  # Fallback for Mac or others

    setup_ui(root)
    root.mainloop()
