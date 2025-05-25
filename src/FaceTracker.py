import cv2
import dlib
import os

class FaceTracker:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector();

        model_path = os.path.join(os.path.dirname(__file__), '..', 'shape_predictor_68_face_landmarks.dat');
        model_path = os.path.abspath(model_path);

        self.predictor = dlib.shape_predictor(model_path);

    def detect_eyes(self, frame):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);

        # Detect faces
        faces = self.detector(gray);

        # Array to hold points of eyes
        left_eye_points = [];
        right_eye_points = [];

        for face in faces:
            # Predict landmarks for each face
            landmarks = self.predictor(gray, face);

            for n in range(36, 42):
                x, y = landmarks.part(n).x, landmarks.part(n).y;
                left_eye_points.append((x,y));

            for n in range(42, 48):
                x, y = landmarks.part(n).x, landmarks.part(n).y;
                right_eye_points.append((x,y));

            # Sum of the points divided by number of points there are for avg
            left_eye_center = (
                sum(p[0] for p in left_eye_points) // len(left_eye_points), # x-axis of eyes
                sum(p[1] for p in left_eye_points) // len(left_eye_points) # y-axis of eyes
            );

            right_eye_center = (
                sum(p[0] for p in right_eye_points) // len(right_eye_points), # x-axis of eyes
                sum(p[1] for p in right_eye_points) // len(right_eye_points) # y-axis of eyes
            );

            eye_midpoint = (
                (left_eye_center[0] + right_eye_center[0]) // 2,
                (left_eye_center[1] + right_eye_center[1]) // 2
            );

            return left_eye_center, right_eye_center, eye_midpoint;

    def draw_landmarks(self, frame, left_eye_center, right_eye_center, eye_midpoint):
        # Draw points on middle of eyes
        cv2.circle(frame, left_eye_center, 1, (0, 0, 255), -1); # Colors: blue, green, red
        cv2.circle(frame, right_eye_center, 1, (0, 0, 255), -1);
        cv2.circle(frame, eye_midpoint, 1, (255, 0, 0), -1);

        cv2.line(frame, left_eye_center, right_eye_center, (0, 255, 255), 1);

        cv2.putText(frame, f'Midpoint: {eye_midpoint}', (10, 30),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 10);