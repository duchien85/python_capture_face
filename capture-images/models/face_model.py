import insightface
from config import PROVIDERS

def load_face_model():
    print("✅ Providers đang dùng:", PROVIDERS)
    model = insightface.app.FaceAnalysis(name='buffalo_l', providers=PROVIDERS)
    model.prepare(ctx_id=-1, det_size=(640, 640))
    return model

# Singleton pattern (load 1 lần dùng chung)
face_model = load_face_model()
