# Load the pre-trained face detector from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat') # Load shape predictor
use_esp32 = True # Set to True if using ESP32 CAM, False for local webcam

# CHANGE PORT ACCORDING TO CONNECTION
port = 'COM5'

# Baudrate for Arduino
baudrate = 9600

# Start webcam (initial testing of head tracker)
# cap = cv2.VideoCapture(0)

# Using esp webserver
ESP32_CAM_IP = "192.168.4.1" # Change to your ESP32 CAM IP address
stream_url = f'http://{ESP32_CAM_IP}/stream'

cap = cv2.VideoCapture(stream_url)

# Frame dimensions
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Smoothing factor for servo movement
smoothing = 0.2

# Max servo angles
servo_min = 0
servo_max = 180