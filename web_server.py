from flask import Flask, render_template_string, Response, stream_with_context
import cv2
import time
from ascii_engine import set_ascii_style, resize_frame, frame_to_ascii
from default_settings import DEFAULTS
from config import GRAPHICS_LEVELS

app = Flask(__name__)
set_ascii_style(DEFAULTS["ascii_style"])

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>VisText</title>
    <style>
        body {
            background-color: black;
            color: lime;
            font-family: monospace;
            white-space: pre;
            font-size: 10px;
            margin: 0;
            padding: 0;
        }
        #ascii {
            line-height: 1;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div id="ascii">Connecting...</div>
    <script>
        const asciiDiv = document.getElementById("ascii");
        const eventSource = new EventSource("/stream");
        eventSource.onmessage = function(event) {
            asciiDiv.innerText = event.data.replace(/\\\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n").replace(/\\n/g, "\\n");
        };
    </script>
</body>
</html>
"""

def generate_ascii_stream():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        yield "data: Error: Cannot open webcam\n\n"
        return

    width = DEFAULTS["ascii_width"]
    quality = GRAPHICS_LEVELS[DEFAULTS["graphics_quality"]]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = resize_frame(gray, new_width=width, char_density=quality)
        ascii_art = "\n".join(frame_to_ascii(resized))

        ascii_escaped = ascii_art.replace("\\", "\\\\").replace("\n", "\\n")
        yield f"data: {ascii_escaped}\n\n"
        time.sleep(1 / DEFAULTS["fps_cap"])

    cap.release()

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/stream")
def stream():
    return Response(stream_with_context(generate_ascii_stream()), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=False, threaded=True)
