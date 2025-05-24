
# 🎥 VisText - Real-Time ASCII Visualizer

VisText is a Python-based tool that converts live webcam, video, or image input into real-time ASCII art — displayed directly in your GUI. Built with OpenCV and Tkinter, it's lightweight, interactive, and fully customizable.

---

## ✨ Features

- 🔁 Live webcam or video-to-text visualization
- 🖼 Convert images or videos to dynamic ASCII
- ⚙️ Real-time font zoom, quality, and resolution controls
- 🔍 Fit-to-window rendering without losing detail
- 🎛 Toggleable floating settings menu
- 🎥 Mirrored webcam feed for natural preview
- 🖱️ Drag-to-pan and scrollable ASCII output
- 📈 FPS counter to track performance
- 🌗 Light/dark-ready interface

---

## 📦 Installation

```bash
pip install opencv-python
pip install pillow
```

No additional libraries required — just standard `tkinter`, which comes with Python.

---

## 🚀 How to Run

```bash
python main.py
```

### Available Modes:
- **Webcam** – Launches webcam stream as ASCII
- **Video** – Load and play any `.mp4`, `.avi`, etc.
- **Image** – View any image as ASCII (JPG, PNG)

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

🖤 Enjoy turning visuals into text.
