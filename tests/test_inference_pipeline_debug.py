import io
import sys
import unittest
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app

class TestInferencePipelineDebug(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_jpg_inference_pipeline(self):
        """Test JPG image through full decoding, preprocessing, and TFLite inference."""
        jpg_path = REPO_ROOT / "ml_model" / "sample_images" / "banana_sample.jpg"
        with open(jpg_path, "rb") as f:
            resp = self.client.post(
                "/scan?lang=en",
                files={"file": ("banana_sample.jpg", f, "image/jpeg")},
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("debug_info", data)
        dbg = data["debug_info"]

        print("\n--- [JPG INFERENCE PIPELINE VERIFICATION] ---")
        print(f" • Received Filename    : {dbg['received_filename']}")
        print(f" • Image Format         : {dbg['image_format']}")
        print(f" • Image Dimensions     : {dbg['image_dimensions'][0]}x{dbg['image_dimensions'][1]}")
        print(f" • Model Input Shape    : {dbg['model_input_shape']}")
        print(f" • Model Input Dtype    : {dbg['model_input_dtype']}")
        print(f" • Output Tensor Shape  : {dbg['output_tensor_shape']}")
        print(f" • Predicted Class Index: {dbg['predicted_class_index']}")
        print(f" • Predicted Class Label: {dbg['predicted_class_label']}")
        print(f" • Confidence           : {dbg['confidence'] * 100:.2f}%")

        self.assertEqual(dbg["image_format"].upper(), "JPEG")
        self.assertEqual(dbg["model_input_shape"], [1, 224, 224, 3])
        self.assertEqual(dbg["model_input_dtype"], "float32")
        self.assertEqual(dbg["output_tensor_shape"], [1, 17])
        self.assertEqual(dbg["predicted_class_label"], "banana")
        self.assertGreaterEqual(dbg["confidence"], 0.60)

    def test_png_inference_pipeline(self):
        """Test PNG image through full decoding, preprocessing, and TFLite inference."""
        img = Image.new("RGB", (300, 300), color="green")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        resp = self.client.post(
            "/scan?lang=en",
            files={"file": ("green_box.png", buf, "image/png")},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("debug_info", data)
        dbg = data["debug_info"]

        print("\n--- [PNG INFERENCE PIPELINE VERIFICATION] ---")
        print(f" • Received Filename    : {dbg['received_filename']}")
        print(f" • Image Format         : {dbg['image_format']}")
        print(f" • Image Dimensions     : {dbg['image_dimensions'][0]}x{dbg['image_dimensions'][1]}")
        print(f" • Model Input Shape    : {dbg['model_input_shape']}")
        print(f" • Model Input Dtype    : {dbg['model_input_dtype']}")
        print(f" • Output Tensor Shape  : {dbg['output_tensor_shape']}")
        print(f" • Predicted Class Index: {dbg['predicted_class_index']}")
        print(f" • Predicted Class Label: {dbg['predicted_class_label']}")
        print(f" • Confidence           : {dbg['confidence'] * 100:.2f}%")

        self.assertEqual(dbg["image_format"].upper(), "PNG")
        self.assertEqual(dbg["model_input_shape"], [1, 224, 224, 3])

    def test_known_food_tomato_inference_pipeline(self):
        """Test Known Food Image (Tomato) through full decoding, preprocessing, and TFLite inference."""
        tomato_path = REPO_ROOT / "ml_model" / "sample_images" / "tomato_sample.jpg"
        with open(tomato_path, "rb") as f:
            resp = self.client.post(
                "/scan?lang=en",
                files={"file": ("tomato_sample.jpg", f, "image/jpeg")},
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("debug_info", data)
        dbg = data["debug_info"]

        print("\n--- [KNOWN FOOD (TOMATO) INFERENCE PIPELINE VERIFICATION] ---")
        print(f" • Received Filename    : {dbg['received_filename']}")
        print(f" • Image Format         : {dbg['image_format']}")
        print(f" • Image Dimensions     : {dbg['image_dimensions'][0]}x{dbg['image_dimensions'][1]}")
        print(f" • Model Input Shape    : {dbg['model_input_shape']}")
        print(f" • Model Input Dtype    : {dbg['model_input_dtype']}")
        print(f" • Output Tensor Shape  : {dbg['output_tensor_shape']}")
        print(f" • Predicted Class Index: {dbg['predicted_class_index']}")
        print(f" • Predicted Class Label: {dbg['predicted_class_label']}")
        print(f" • Confidence           : {dbg['confidence'] * 100:.2f}%")

        self.assertEqual(dbg["predicted_class_label"], "tomato")
        self.assertGreaterEqual(dbg["confidence"], 0.60)

if __name__ == "__main__":
    unittest.main()
