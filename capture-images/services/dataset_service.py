import cv2
import os
import shutil
from config import DATASET_DIR, MAX_IMAGES
from utils.logger import logger

def delete_dataset(person_name: str, save_path: str) -> dict:
    """
    Xóa toàn bộ dữ liệu của một person_name.
    Trả về dict chứa status + message.
    """
    try:
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
            logger.info(f"Đã xóa dataset của {person_name} tại {save_path}")
            return {"status": "ok", "message": f"Đã xóa toàn bộ dữ liệu của {person_name}"}
        else:
            logger.warning(f"Không tìm thấy dataset cho {person_name} tại {save_path}")
            return {"status": "not_found", "message": f"Không tìm thấy dữ liệu cho {person_name}"}
    except Exception as e:
        logger.exception("Lỗi khi xóa dataset")
        return {"status": "error", "message": str(e)}
def get_save_path(person_name):
    return os.path.join(DATASET_DIR, person_name)

def reset_dataset(person_name):
    save_path = get_save_path(person_name)
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path, exist_ok=True)

def count_images(person_name):
    save_path = get_save_path(person_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
        return 0
    return len([f for f in os.listdir(save_path) if f.lower().endswith(".jpg")])

def save_face_image(person_name, frame, bbox, filename):
    x1, y1, x2, y2 = bbox
    face_crop = frame[y1:y2, x1:x2]
    save_path = get_save_path(person_name)
    os.makedirs(save_path, exist_ok=True)
    cv2.imwrite(os.path.join(save_path, filename), face_crop)
