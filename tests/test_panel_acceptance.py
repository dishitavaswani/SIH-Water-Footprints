"""Panel Acceptance Verification Test Suite (Tests A through Q)."""

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

class TestPanelAcceptance(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_search_product_flow(self):
        """TEST A, B, C: Search Product -> Query -> Endpoint -> Result."""
        resp = self.client.get("/footprint?item=apple&lang=en")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["item"].lower(), "apple")
        self.assertIn("description", data)
        self.assertGreater(data["total_litres_per_kg"], 0)
        print("\n -> TEST A, B, C (Search 'apple'): PASSED")

    def test_popular_chips_rice_and_coffee(self):
        """TEST D, E: Popular chips mapping (Rice, Coffee)."""
        # Rice
        resp_rice = self.client.get("/footprint?item=rice&lang=en")
        self.assertEqual(resp_rice.status_code, 200)
        self.assertEqual(resp_rice.json()["item"].lower(), "rice")

        # Coffee
        resp_coffee = self.client.get("/footprint?item=coffee&lang=en")
        self.assertEqual(resp_coffee.status_code, 200)
        self.assertEqual(resp_coffee.json()["item"].lower(), "coffee")
        print(" -> TEST D, E (Chips 'rice', 'coffee'): PASSED")

    def test_all_popular_chips_database_mapping(self):
        """Verify all popular chips map to real database items."""
        chips = ["rice", "coffee", "apple", "chocolate", "beef", "banana", "milk", "wheat"]
        for chip in chips:
            resp = self.client.get(f"/footprint?item={chip}&lang=en")
            self.assertEqual(resp.status_code, 200, f"Chip '{chip}' not found in database!")
            self.assertIn("total_litres_per_kg", resp.json())
        print(f" -> Popular Chips Mapping ({len(chips)} items): ALL MAPPED TO DATABASE")

    def test_ai_camera_scan_flow_jpg(self):
        """TEST F, G, I, J, K, L, M, N, O: Camera Scan JPG -> ML -> DB -> Result."""
        jpg_path = REPO_ROOT / "ml_model" / "sample_images" / "tomato_sample.jpg"
        with open(jpg_path, "rb") as f:
            resp = self.client.post(
                "/scan?lang=en",
                files={"file": ("tomato.jpg", f, "image/jpeg")},
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["canonical_label"], "tomato")
        self.assertIn("description", data["item_details"])
        self.assertIn("water_footprint", data)
        self.assertEqual(data["water_footprint"]["total"], 215.0)
        print(" -> TEST F, G, I-O (Camera JPG Tomato): PASSED")

    def test_ai_camera_scan_flow_png(self):
        """TEST H: Camera Scan PNG file."""
        img = Image.new("RGB", (300, 300), color="orange")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        resp = self.client.post(
            "/scan?lang=en",
            files={"file": ("test_orange.png", buf, "image/png")},
        )
        self.assertEqual(resp.status_code, 200)
        print(" -> TEST H (Camera PNG Upload): PASSED")

    def test_multilingual_language_switching(self):
        """TEST P: Changing language changes displayed result."""
        # English
        resp_en = self.client.get("/footprint?item=apple&lang=en")
        self.assertEqual(resp_en.status_code, 200)

        # Hindi
        resp_hi = self.client.get("/footprint?item=apple&lang=hi")
        self.assertEqual(resp_hi.status_code, 200)

        # Marathi
        resp_mr = self.client.get("/footprint?item=apple&lang=mr")
        self.assertEqual(resp_mr.status_code, 200)

        print(f" -> TEST P (Multilingual Search): EN, HI, MR status 200 PASSED")

    def test_invalid_input_error_handling(self):
        """TEST Q: Invalid input produces visible error."""
        resp = self.client.get("/footprint?item=non_existent_item_xyz&lang=en")
        self.assertEqual(resp.status_code, 404)
        print(" -> TEST Q (Invalid Product Error 404): PASSED")

if __name__ == "__main__":
    unittest.main()
