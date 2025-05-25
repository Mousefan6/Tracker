import cv2
import sys
from src.config import *
import numpy as np
import requests
import time

from src.FaceTracker import FaceTracker
from src.ServoController import ServoController

# === Logger Setup ===
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    camera = cv2.VideoCapture(STREAM_URL);
    controller = ServoController(port='COM5')
    if not camera.isOpened():
        print("Error: Could not open video stream.");
        sys.exit(1);
    
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.SpecialFilter, 2)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)
    
    faceTracker = FaceTracker();

    # Initial servo positions
    previous_x_angle = 90;
    previous_y_angle = 45;

    # Bring servos to default positions
    controller.send_coordinates(previous_x_angle, previous_y_angle)
    time.sleep(0.5)

    frame_count = 0 # To avoid overloading arduino

    try:
        while True:
            ret, frame = camera.read();
            if not ret:
                print("FATAL: Could not read frame from camera's web server.");
                break;
            
            if frame is None or frame.size == 0:
                print("Dirty frame received. Skipping...");
                continue

            frame_count += 1
            
            detect_eyes = faceTracker.detect_eyes(frame);
            if detect_eyes is None: # No face detected display as normal
                cv2.imshow("Head Tracker", frame);
                cv2.waitKey(1); # Prevent cv2 throttling
                continue;
            
            left_eye, right_eye, midpoint = detect_eyes; # Dereference the tuple
            
            # Get midpoint for servo angles
            x_norm = midpoint[0] / frame.shape[1];
            y_norm = midpoint[1] / frame.shape[0];

            # Calculate servo angles
            x_angle = int(SERVO_X_MIN + (SERVO_X_MAX - SERVO_X_MIN) * x_norm);
            y_angle = int(SERVO_Y_MIN + (SERVO_Y_MAX - SERVO_Y_MIN) * y_norm);
            
            # Movement smoothing
            smoothed_x = int(previous_x_angle + SERVO_SMOOTHING * (x_angle - previous_x_angle));
            smoothed_y = int(previous_y_angle + SERVO_SMOOTHING * (y_angle - previous_y_angle));
            
            # Update previous angles
            previous_x_angle = smoothed_x;
            previous_y_angle = smoothed_y;

            # Send data to arduino
            if controller.send_coordinates(smoothed_x, smoothed_y):
                logger.debug(f"Sent servo angles: X={smoothed_x}, Y={smoothed_y}")
            else:
                logger.warning("Failed to send servo coordinates")

            # Visualization of midpoint of eyes
            cv2.circle(frame, midpoint, 3, (255, 0, 0), -1);
            cv2.putText(frame, f'Angle: ({smoothed_x}, {smoothed_y})', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2);

            cv2.imshow("Head Tracker", frame);
            cv2.waitKey(1); # Prevent cv2 throttling
    
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Exiting...");
    finally:
        if controller:
            # Return servos to center position before closing
            controller.send_coordinates(90, 45)
            time.sleep(0.5)
            controller.close()
            
        # Release resources
        camera.release();
        cv2.destroyAllWindows();

if __name__ == "__main__":
    main()