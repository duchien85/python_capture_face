import onnxruntime as ort

# DATASET_DIR = "dataset_faces"
DATASET_DIR = "../dataset_faces"
MAX_IMAGES = 50

# Provider ưu tiên (CoreML trước, fallback CPU)
available_providers = ort.get_available_providers()
if "CoreMLExecutionProvider" in available_providers:
    PROVIDERS = [("CoreMLExecutionProvider", {"enable_fp16": True}), "CPUExecutionProvider"]
else:
    PROVIDERS = ["CPUExecutionProvider"]
