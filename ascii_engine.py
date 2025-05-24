import cv2
from config import ASCII_CHARS

def resize_frame(frame, new_width, char_density):
    height, width = frame.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * char_density)
    return cv2.resize(frame, (new_width, new_height))

def gray_to_ascii(gray_frame):
    ascii_image = ""
    for row in gray_frame:
        for pixel in row:
            char = ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256]
            ascii_image += char
        ascii_image += "\n"
    return ascii_image

def process_frame(frame, width, char_density):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = resize_frame(gray, width, char_density)
    return gray_to_ascii(resized)
