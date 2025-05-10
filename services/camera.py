import cv2
from config import STREAM_URL, use_esp32, frame_width, frame_height

def setup_camera():
    if use_esp32:
        cap = cv2.VideoCapture(STREAM_URL) # ESP32 CAM stream URL
        cap.set(cv2.CAP_PROP_FPS, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    else:
        cap = cv2.VideoCapture(0)  # Local webcam

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    print("Camera setup complete.")
    return cap