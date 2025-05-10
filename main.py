import cv2
import time
from config import *
from services.camera import setup_camera
from services.servo import ServoController
from services.face_tracker import FaceTracker
from utils.helpers import smooth_angle

def main():
    # Initialize components
    cap = setup_camera()
    servo = ServoController()
    detector = FaceTracker()
    
    previous_angle = 90  # Initial servo position

    try:
        while True:
            ret, frame = cap.read()
            if not ret: # For webserver, if frame is not available, retry
                print("Error: Could not read frame from camera.")
                time.sleep(1)
                cap.release()
                cap = setup_camera()
                if cap is None: # For ESP32 CAM, if the camera is not available, exit the loop
                    print("Error: Camera not available.")
                    break
                break

            for left_eye, right_eye, midpoint in detector.detect_eyes(frame):
                # Map midpoint to servo angle
                x_norm = midpoint[0] / frame.shape[1]
                target_angle = int(servo_min + (servo_max - servo_min) * x_norm)
                
                # Movement smoothing
                smoothed_angle = smooth_angle(previous_angle, target_angle, smoothing)
                servo.move_servo(smoothed_angle)
                previous_angle = smoothed_angle

                # Visualization of midpoint of eyes (optional)
                cv2.circle(frame, midpoint, 3, (255, 0, 0), -1)
                cv2.putText(frame, f'Angle: {smoothed_angle}', (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('Head Tracker', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): # q key to exit
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        servo.close()

if __name__ == "__main__":
    main()