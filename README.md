# 🎥 VisText - Real-Time ASCII Visualizer

VisText is a Python-based tool that converts live webcam, video, or image input into real-time ASCII art — displayed directly in your GUI or streamed to your browser. Built with OpenCV, Tkinter, and Flask, it's lightweight, interactive, and fully customizable.

---

## ✨ Features

- 🔁 Live webcam or video-to-text visualization
- 🖼 Convert images or videos to dynamic ASCII
- ⚡ Motion-aware frame differencing (only updates on real visual change)
- 🧪 CLI tool for converting image to `.txt`, `.html`, or `.png`
- 🌐 Web-compatible: stream ASCII to browser with Flask
- ⚙️ Real-time font zoom, quality, and resolution controls
- 🔍 Fit-to-window rendering without losing detail
- 🎛 Toggleable floating settings menu
- 🖱️ Drag-to-pan and scrollable ASCII output
- 📈 FPS counter to track performance
- 💾 Export frame as `.txt`, `.png`, `.html`
- 🌗 Light/dark-ready interface
- ⚙️ Fully configurable via `default_settings.py`

---

## 📦 Installation

```bash
pip install opencv-python
pip install pillow
pip install flask
```

No additional libraries required — just standard `tkinter`, which comes with Python.

---

## 🚀 How to Run

### GUI Version
```bash
python main.py
```

### Web Version
```bash
python web_server.py
# Then open http://localhost:5000 in your browser
```

### CLI Mode (Image to ASCII)
```bash
python cli.py -i path/to/image.jpg -o output --width 100 --export txt
```

---

## 🎮 Controls

| Control                  | Description                         |
|--------------------------|-------------------------------------|
| `Ctrl + Mouse Wheel`     | Zoom in/out (font size)             |
| `Mouse Wheel`            | Scroll vertically                   |
| `Click + Drag`           | Pan around the ASCII                |
| `Fit to Window` checkbox | Auto-resize resolution to window    |
| `Hide Menu`              | Collapse floating settings panel    |

---

🖤 Enjoy turning visuals into live text.
