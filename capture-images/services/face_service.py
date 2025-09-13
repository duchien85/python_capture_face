from collections import deque
import numpy as np

# Dictionary để lưu history theo session/user
user_ear_history = {}

def eye_aspect_ratio(eye_points):
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])

    if C < 1e-6:
        return 0.0

    return (A + B) / (2.0 * C)

def is_eyes_open(landmarks, user_id="default", threshold=0.25, diff_limit=0.20, debug=True):
    try:
        # Khởi tạo history cho user nếu chưa có
        if user_id not in user_ear_history:
            user_ear_history[user_id] = deque(maxlen=5)

        ear_history = user_ear_history[user_id]

        # Kiểm tra landmarks hợp lệ
        if landmarks is None or len(landmarks) < 76:
            if debug: print("❌ Landmarks không hợp lệ")
            return False

        left_eye_idx = [60, 61, 62, 63, 64, 65, 66, 67]
        right_eye_idx = [68, 69, 70, 71, 72, 73, 74, 75]

        left_eye = np.array([landmarks[i] for i in left_eye_idx])
        right_eye = np.array([landmarks[i] for i in right_eye_idx])

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        mean_ear = (left_ear + right_ear) / 2.0
        diff_ear = abs(left_ear - right_ear)

        # Lưu lịch sử
        ear_history.append((left_ear, right_ear))

        if debug:
            print(f"EAR L:{left_ear:.3f}, R:{right_ear:.3f}, Mean:{mean_ear:.3f}, Diff:{diff_ear:.3f}")

        # 1. Kiểm tra nếu cả 2 mắt nhắm
        if mean_ear < threshold:
            if debug: print("❌ Cả 2 mắt nhắm")
            return False

        # 2. Kiểm tra chênh lệch tức thời
        if diff_ear > diff_limit:
            if debug: print("❌ Chênh lệch EAR giữa 2 mắt quá lớn")
            return False

        return True

    except Exception as e:
        if debug:
            print(f"EAR calc error: {e}")
        return False

def cleanup_user_history(user_id):
    """Dọn dẹp history khi user hoàn thành session"""
    if user_id in user_ear_history:
        del user_ear_history[user_id]