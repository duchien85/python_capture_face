from flask import Blueprint, request, jsonify
import base64, cv2, numpy as np, time, os, shutil, logging
from models.face_model import face_model
from services.face_service import is_eyes_open
from services.dataset_service import reset_dataset, count_images, save_face_image, get_save_path, delete_dataset
from config import MAX_IMAGES

bp = Blueprint("face_routes", __name__)

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

last_reset_time = {}

@bp.route('/upload', methods=['POST'])
def upload():
    person_name = request.form.get('person_name')
    reset = request.form.get('reset') == 'true'
    image_data = request.form.get('image')

    if not person_name or not image_data:
        return jsonify({"status": "error", "message": "Thiếu dữ liệu"}), 400

    # Decode ảnh base64
    try:
        header, encoded = image_data.split(',', 1)
        img_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        logger.exception("Lỗi decode ảnh base64")
        return jsonify({"status": "error", "message": f"Ảnh không hợp lệ: {str(e)}"}), 400

    # Reset nếu có flag
    if reset and (person_name not in last_reset_time or time.time() - last_reset_time[person_name] > 2):
        try:
            reset_dataset(person_name)
            last_reset_time[person_name] = time.time()
        except Exception as e:
            logger.exception("Lỗi reset dataset")
            return jsonify({"status": "error", "message": f"Không reset được dataset: {str(e)}"}), 500

    # Đếm ảnh hiện có
    try:
        count = count_images(person_name)
    except Exception as e:
        logger.exception("Lỗi đếm ảnh dataset")
        return jsonify({"status": "error", "message": f"Không đếm được ảnh: {str(e)}"}), 500

    if count >= MAX_IMAGES:
        return jsonify({"status": "done", "message": f"Đã đủ {MAX_IMAGES} ảnh", "count": count})

    # Detect khuôn mặt
    try:
        faces = face_model.get(frame)
    except Exception as e:
        logger.exception("Lỗi detect khuôn mặt")
        return jsonify({"status": "error", "message": f"Lỗi detect khuôn mặt: {str(e)}"}), 500

    if len(faces) == 0:
        return jsonify({"status": "no_face", "message": "Không tìm thấy khuôn mặt", "count": count})

    face = faces[0]

    # Giả sử anh có hàm get_landmarks(frame) → trả về 68 points
    # threshold = calibrate_threshold(lambda: get_landmarks(frame), duration=5)

    # Sau đó dùng threshold này để kiểm tra mắt mở
    # is_eyes_open(face_landmarks, threshold=threshold)

    # face.landmark_2d_106 → landmarks (106 điểm, chứ không phải 68).
    if not is_eyes_open(face.landmark_2d_106):
        return jsonify({"status": "eyes_closed", "message": "Mắt nhắm, không lưu ảnh", "count": count})

    next_num = count + 1
    # filename = f"{person_name}_{next_num:03d}.jpg"
    filename = f"{next_num:02d}.jpg"
    bbox = face.bbox.astype(int).tolist()

    try:
        save_face_image(person_name, frame, bbox, filename)
    except Exception as e:
        logger.exception("Lỗi lưu ảnh khuôn mặt")
        return jsonify({"status": "error", "message": f"Không lưu được ảnh: {str(e)}"}), 500

    return jsonify({
        "status": "ok",
        "message": f"Đã lưu {filename}",
        "filename": filename,
        "bbox": bbox,
        "count": next_num
    })

# @bp.route('/delete', methods=['POST'])
# def delete():
#     person_name = request.form.get('person_name')
#
#     if not person_name:
#         return jsonify({"status": "error", "message": "Thiếu person_name"}), 400
#
#     save_path = get_save_path(person_name)
#
#     try:
#         if os.path.exists(save_path):
#             shutil.rmtree(save_path)
#             return jsonify({"status": "ok", "message": f"Đã xóa toàn bộ dữ liệu của {person_name}"})
#         else:
#             return jsonify({"status": "not_found", "message": f"Không tìm thấy dữ liệu cho {person_name}"})
#     except Exception as e:
#         logger.exception("Lỗi khi xóa dataset")
#         return jsonify({"status": "error", "message": str(e)}), 500
@bp.route('/delete', methods=['POST'])
def delete():
    person_name = request.form.get('person_name')

    if not person_name:
        return jsonify({"status": "error", "message": "Thiếu person_name"}), 400

    save_path = get_save_path(person_name)

    result = delete_dataset(person_name, save_path)

    if result["status"] == "error":
        return jsonify(result), 500
    return jsonify(result)
