from insightface.app import FaceAnalysis
import cv2
import numpy as np

def eye_aspect_ratio(eye_points):
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Dùng buffalo_sc để có 106 landmarks
app = FaceAnalysis(name='buffalo_sc')
app.prepare(ctx_id=0, det_size=(640, 640))

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)
    for face in faces:
        if face.landmark is None:
            continue   # bỏ qua nếu không có landmark

        lm = face.landmark.astype(int)

        left_eye = lm[60:68]
        right_eye = lm[68:76]

        # Vẽ landmarks mắt
        for idx, (x, y) in enumerate(left_eye, start=60):
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
            cv2.putText(frame, str(idx), (x+2, y-2),
                        cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1)

        for idx, (x, y) in enumerate(right_eye, start=68):
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            cv2.putText(frame, str(idx), (x+2, y-2),
                        cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0), 1)

        # EAR
        ear_left = eye_aspect_ratio(left_eye)
        ear_right = eye_aspect_ratio(right_eye)
        ear_mean = (ear_left + ear_right) / 2.0

        cv2.putText(frame, f"EAR L:{ear_left:.3f} R:{ear_right:.3f} M:{ear_mean:.3f}",
                    (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("EAR Debug", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()