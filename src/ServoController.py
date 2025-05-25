# This file is for testing the servos for x and y direction to see
# if they are responsive and connects the arduino IDE

import serial
import time
import struct
import logging

logger = logging.getLogger(__name__)

class ServoController:
    def __init__(self, port='COM5', baudrate=9600):
        self.arduino = serial.Serial(port, baudrate, timeout=0.1)
        time.sleep(2)

        logger.info(f"Connected to Arduino on {port} at {baudrate} baud")
        self.arduino.flushInput()
        self.arduino.flushOutput()

    def send_coordinates(self, x, y):
        x = max(0, min(180, x))  # Constrain to servo range
        y = max(0, min(180, y))
        self.arduino.write(struct.pack('BB', x, y))  # 'BB' = 2 unsigned bytes for faster communication
        self.arduino.flush()
        # For debugging    
        logger.debug(f"Sent coordinates: X={x}, Y={y}")
        return self._read_response()
    
    def _read_response(self):
        # Optionally read response from arduino
        if self.arduino.in_waiting > 0:
            return self.arduino.readline().decode().strip()
        return None
    
    def close(self):
        self.arduino.close()

# Example test for running
# if __name__ == "__main__":
#     controller = ServoController()
#     try:
#         while True:
#             try:
#                 coords = input("Enter coordinates in format x,y: ")
#                 x, y = map(int, coords.split(',')) # maps x and y

#                 # Send the coord to arduino IDE
#                 response = controller.send_coordinates(x, y)
#             except ValueError:
#                 print("Wrong format")
#     except KeyboardInterrupt:
#         print("\nClosing connection")
#         controller.close()