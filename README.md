# Tracker

## Overview
This project uses the ESP32-CAM module to track a face and move servos accordingly.

## Installation

### Local Setup
1. **Clone the repository:**
```sh
git clone <your-repo-url>
cd <your-repo-name>
```

2. **Create a virtual environment (optional but recommended):**
```
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. **Install CMake on your device:**

[Download CMake installer here (if not done so already)](https://cmake.org/download/)

Validate its installation:
```sh
cmake --version
```

4. **Install dependencies:**
```sh
pip install -r requirements.txt
```

## Specs

### Camera Module
```sh
ESP32-CAM Development Board
```

### Servo Module
```sh
INSERT
```


## Usage
Ensure that your current working directory is set to the project's root directory in the terminal of your choice.

### Compiling
```sh
python main.py
```


## Troubleshooting
- Ensure that you have activated the virtual environment with the installed packages.
- Ensure CMake is installed on your system.
- Ensure `shape_predictor_68_face_landmarks.dat` exists.
- Clear `__pycache__` and compile again.


## License
This project is licensed under the MIT License.