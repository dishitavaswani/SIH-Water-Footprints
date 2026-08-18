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

class TestLensUploadDiagnostic(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_upload_test_endpoint_jpg(self):
        img = Image.new("RGB", (300, 300), color="red")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        resp = self.client.post(
            "/upload-test",
            files={"file": ("rice.jpg", buf, "image/jpeg")},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["filename"], "rice.jpg")
        self.assertEqual(data["content_type"], "image/jpeg")
        self.assertGreater(data["size"], 0)
        print("\n -> POST /upload-test JPG: SUCCESS (filename: rice.jpg, size:", data["size"], "bytes)")

    def test_upload_test_endpoint_png(self):
        img = Image.new("RGB", (300, 300), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        resp = self.client.post(
            "/upload-test",
            files={"file": ("banana.png", buf, "image/png")},
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["filename"], "banana.png")
        self.assertEqual(data["content_type"], "image/png")
        print(" -> POST /upload-test PNG: SUCCESS (filename: banana.png, size:", data["size"], "bytes)")

    def test_scan_endpoint_jpg(self):
        jpg_path = REPO_ROOT / "ml_model" / "sample_images" / "tomato_sample.jpg"
        with open(jpg_path, "rb") as f:
            resp = self.client.post(
                "/scan?lang=en",
                files={"file": ("tomato_sample.jpg", f, "image/jpeg")},
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["canonical_label"], "tomato")
        print(" -> POST /scan JPG (Tomato): SUCCESS (canonical_label: tomato, confidence:", data["confidence"], ")")

if __name__ == "__main__":
    unittest.main()
