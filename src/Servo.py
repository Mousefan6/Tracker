import serial
import time
import numpy as np
from config import port, baudrate, servo_min, servo_max, smoothing

class ServoController:
    def __init__(self, port=port, baudrate=baudrate):
        self.arduino = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for the connection to establish
        
    def move_servo(self, angle):
        angle = np.clip(angle, servo_min, servo_max)  # Constrain angle
        self.arduino.write(f"{angle}\n".encode()) # Format the angle as a string and send it to Arduino as "30\n" for instance
        response = self.arduino.readline().decode().strip()
        print(f"Servo angle: {angle} | Response: {response}")
    
    def close(self):
        self.arduino.close()
        print("Serial connection closed.")