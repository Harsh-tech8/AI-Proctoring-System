import sys

import numpy as np

sys.path.insert(0, r"c:\Users\harsh\Downloads\AI-Proctoring-System-Complete\AI-Proctoring-System\services\vision_worker")

import app.detector as d


def main():
    d.EYE_CASCADE.detectMultiScale = lambda *args, **kwargs: [(0, 0, 20, 20)]
    face = np.zeros((120, 200, 3), dtype=np.uint8)
    score = d.detect_gaze(face[:, :, 0], face)
    print(f"gaze_score={score}")
    print(f"threshold={d.LOOK_AWAY_THRESHOLD}")


if __name__ == "__main__":
    main()
