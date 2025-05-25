import cv2
import sys
from src.config import *
import numpy as np
import requests
import time

from src.FaceTracker import FaceTracker

# === Logger Setup ===
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    camera = cv2.VideoCapture(STREAM_URL);
    if not camera.isOpened():
        print("Error: Could not open video stream.");
        sys.exit(1);
    
    faceTracker = FaceTracker();

    previous_angle = 0;  # Initial servo position

    try:
        while True:
            ret, frame = camera.read();
            if not ret:
                print("FATAL: Could not read frame from camera's web server.");
                break;
            
            if frame is None or frame.size == 0:
                print("Dirty frame received. Skipping...");
                continue
            
            detect_eyes = faceTracker.detect_eyes(frame);
            if detect_eyes is None: # No face detected display as normal
                cv2.imshow("Head Tracker", frame);
                cv2.waitKey(1); # Prevent cv2 throttling
                continue;
            
            left_eye, right_eye, midpoint = detect_eyes; # Dereference the tuple
            
            # Map midpoint to servo angle
            x_norm = midpoint[0] / frame.shape[1];
            target_angle = int(SERVO_MIN + (SERVO_MAX - SERVO_MIN) * x_norm);
            
            # Movement smoothing
            smoothed_angle = int(previous_angle + SERVO_SMOOTHING * (target_angle - previous_angle));
            previous_angle = smoothed_angle;

            # Visualization of midpoint of eyes
            cv2.circle(frame, midpoint, 3, (255, 0, 0), -1);
            cv2.putText(frame, f'Angle: {smoothed_angle}', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2);

            cv2.imshow("Head Tracker", frame);
            cv2.waitKey(1); # Prevent cv2 throttling
    
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Exiting...");
    finally:
        # Release resources
        camera.release();
        cv2.destroyAllWindows();


if __name__ == "__main__":
    main();
