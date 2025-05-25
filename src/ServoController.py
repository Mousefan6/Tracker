# This file is for testing the servos for x and y direction to see
# if they are responsive and connects the arduino IDE
import serial
import time

class ServoController:
    def __init__(self, port='COM5', baudrate=9600):
        self.arduino = serial.Serial(port, baudrate, timeout=0.1)
        time.sleep(2)

    def send_coordinates(self, x, y):
        coord = f"{x}, {y},\n"
        self.arduino.write(coord.encode('utf-8'))
        return self._read_response()
    
    def _read_response(self):
        response = []
        start_time = time.time()
        
        # Read for up to 1 second
        while time.time() - start_time < 1:
            if self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode('utf-8').strip()
                if line:
                    response.append(line)
        
        return '\n'.join(response) if response else "No response"
    
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