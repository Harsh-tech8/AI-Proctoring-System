import base64
import os
from dataclasses import dataclass, asdict

import cv2
import numpy as np

LOOK_AWAY_THRESHOLD = float(os.getenv("LOOK_AWAY_THRESHOLD", "0.45"))

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
EYE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

@dataclass
class Detection:
    signal: str
    severity: int
    confidence: float
    message: str

def decode_frame(frame_base64: str):
    raw = frame_base64.split(",", 1)[-1]
    data = base64.b64decode(raw)
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    return image

def detect_gaze(face_gray, face_color):
    eyes = EYE_CASCADE.detectMultiScale(
        face_gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(16, 16),
    )
    if len(eyes) == 0:
        # A detected face without a usable eye pair is treated as suspicious in a
        # proctoring context, because gaze is critical and the camera often blurs or
        # partially hides the user's face when they look away.
        return 0.55

    fx = face_color.shape[1] / 2
    centers = [x + w / 2 for x, y, w, h in eyes[:2]]
    eye_center = sum(centers) / len(centers)
    normalized = abs(eye_center - fx) / max(fx, 1)

    if normalized > LOOK_AWAY_THRESHOLD:
        return min(1.0, normalized)
    return 0.0

def analyze(frame_base64: str):
    image = decode_frame(frame_base64)
    if image is None:
        return [Detection("CAMERA_ERROR", 3, 1.0, "Camera frame could not be decoded")]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
    )

    if len(faces) == 0:
        return [Detection("NO_FACE", 3, 0.95, "No face detected in the camera frame")]

    if len(faces) > 1:
        return [Detection(
            "MULTIPLE_FACES", 5, min(1.0, 0.7 + len(faces) * 0.1),
            f"{len(faces)} faces detected"
        )]

    x, y, w, h = faces[0]
    face_gray = gray[y:y+h, x:x+w]
    face_color = image[y:y+h, x:x+w]
    eyes = EYE_CASCADE.detectMultiScale(
        face_gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(16, 16),
    )

    if len(eyes) < 2:
        return [Detection(
            "EYE_CLOSED",
            2,
            0.8,
            "Eyes are not clearly visible; candidate may be blinking or looking away"
        )]

    gaze = detect_gaze(face_gray, face_color)

    if gaze is not None and gaze > LOOK_AWAY_THRESHOLD:
        return [Detection(
            "LOOKING_AWAY", 2, gaze,
            "Possible gaze divergence detected"
        )]

    if gaze is not None and gaze > 0:
        return [Detection(
            "NORMAL", 0, 0.90, "No cheat signal detected; gaze is within tolerance"
        )]

    return [Detection("NORMAL", 0, 0.90, "No configured cheat signal detected")]
