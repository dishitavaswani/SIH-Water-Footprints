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

class TestImageUploadPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_upload_valid_jpeg(self):
        img = Image.new("RGB", (300, 300), color="red")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        response = self.client.post(
            "/scan?lang=en",
            files={"file": ("test_photo.jpg", buf, "image/jpeg")},
        )
        if response.status_code != 200:
            print("JPEG ERROR:", response.status_code, response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("success", data)

    def test_upload_valid_png(self):
        img = Image.new("RGB", (200, 200), color="green")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        response = self.client.post(
            "/scan?lang=en",
            files={"file": ("test_photo.png", buf, "image/png")},
        )
        self.assertEqual(response.status_code, 200)

    def test_upload_valid_webp(self):
        img = Image.new("RGB", (200, 200), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="WEBP")
        buf.seek(0)

        response = self.client.post(
            "/scan?lang=en",
            files={"file": ("test_photo.webp", buf, "image/webp")},
        )
        self.assertEqual(response.status_code, 200)

    def test_upload_non_image_file(self):
        text_buf = io.BytesIO(b"This is a text file, not an image.")
        response = self.client.post(
            "/scan?lang=en",
            files={"file": ("document.txt", text_buf, "text/plain")},
        )
        self.assertIn(response.status_code, [400, 415])

    def test_upload_corrupted_image(self):
        corrupt_buf = io.BytesIO(b"GIF89a\x00\x00\x00corrupted_bytes_12345")
        response = self.client.post(
            "/scan?lang=en",
            files={"file": ("corrupt.jpg", corrupt_buf, "image/jpeg")},
        )
        self.assertEqual(response.status_code, 400)

    def test_upload_image_without_content_type(self):
        """Even if content-type header is octet-stream, valid image bytes with .jpg extension should be handled or validated."""
        img = Image.new("RGB", (200, 200), color="yellow")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        response = self.client.post(
            "/scan?lang=en",
            files={"file": ("camera_photo.jpg", buf, "application/octet-stream")},
        )
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
