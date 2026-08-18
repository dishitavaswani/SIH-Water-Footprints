"""Test suite for Water Impact Insights layer (Section 14 verification)."""

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
from backend.app.services.insights_service import (
    calculate_volumetric_comparison,
    calculate_impact_severity,
    calculate_alternative_savings,
    generate_water_impact_insights,
)

class TestWaterImpactInsights(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_rice_insights(self):
        """Test Rice insights calculation."""
        res = generate_water_impact_insights("rice", 990, 480, 130)
        self.assertEqual(res["total_litres"], 1600.0)
        self.assertEqual(res["comparison"]["benchmark"], "bathtub")
        self.assertEqual(res["comparison"]["display_quantity"], 11)
        self.assertEqual(res["comparison"]["display_text"], "≈ 11 bathtubs")
        self.assertEqual(res["severity"]["level"], "high")
        self.assertTrue(res["alternative"]["has_alternative"])
        self.assertEqual(res["alternative"]["name"], "Wheat")
        self.assertEqual(res["alternative"]["savings_percentage"], 29)
        print("\n -> Rice Insights (1600 L): PASSED (~ 11 bathtubs, High Impact, 29% savings with Wheat)")

    def test_coffee_insights(self):
        """Test Coffee insights calculation."""
        res = generate_water_impact_insights("coffee", 11000, 5000, 2000)
        self.assertEqual(res["total_litres"], 18000.0)
        self.assertEqual(res["comparison"]["benchmark"], "swimming_pool")
        self.assertEqual(res["comparison"]["display_quantity"], 1)
        self.assertEqual(res["severity"]["level"], "very_high")
        self.assertTrue(res["alternative"]["has_alternative"])
        self.assertEqual(res["alternative"]["name"], "Tea")
        self.assertEqual(res["alternative"]["savings_percentage"], 51)
        print(" -> Coffee Insights (18000 L): PASSED (~ 1 swimming pool, Very High Impact, 51% savings with Tea)")

    def test_beef_insights(self):
        """Test Beef insights calculation."""
        res = generate_water_impact_insights("beef", 14000, 1000, 450)
        self.assertEqual(res["total_litres"], 15450.0)
        self.assertEqual(res["severity"]["level"], "very_high")
        self.assertEqual(res["alternative"]["name"], "Chicken")
        self.assertEqual(res["alternative"]["savings_percentage"], 72)
        print(" -> Beef Insights (15450 L): PASSED (Very High Impact, 72% savings with Chicken)")

    def test_small_footprint_tomato(self):
        """Test small footprint Tomato calculation."""
        res = generate_water_impact_insights("tomato", 108, 64, 43)
        self.assertEqual(res["total_litres"], 215.0)
        self.assertEqual(res["comparison"]["benchmark"], "bucket")
        self.assertEqual(res["comparison"]["display_quantity"], 14)
        self.assertEqual(res["severity"]["level"], "low")
        print(" -> Tomato Insights (215 L): PASSED (~ 14 buckets, Low Impact)")

    def test_api_endpoint_search_insights(self):
        """Test GET /footprint returns complete insights dictionary."""
        resp = self.client.get("/footprint?item=rice&lang=en")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("insights", data)
        ins = data["insights"]
        self.assertIn("comparison", ins)
        self.assertIn("severity", ins)
        self.assertIn("alternative", ins)
        self.assertIn("explanation", ins)
        print(" -> API GET /footprint Insights Structure: PASSED")

    def test_api_endpoint_scan_insights(self):
        """Test POST /scan returns complete insights dictionary."""
        jpg_path = REPO_ROOT / "ml_model" / "sample_images" / "tomato_sample.jpg"
        with open(jpg_path, "rb") as f:
            resp = self.client.post(
                "/scan?lang=en",
                files={"file": ("tomato.jpg", f, "image/jpeg")},
            )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertIn("insights", data)
        print(" -> API POST /scan Insights Structure: PASSED")

    def test_multilingual_insights_translation(self):
        """Test Hindi and Marathi insights translation."""
        resp_hi = self.client.get("/footprint?item=rice&lang=hi")
        self.assertEqual(resp_hi.status_code, 200)
        ins_hi = resp_hi.json()["insights"]
        self.assertIn("insights", resp_hi.json())

        resp_mr = self.client.get("/footprint?item=rice&lang=mr")
        self.assertEqual(resp_mr.status_code, 200)
        self.assertIn("insights", resp_mr.json())

        print(" -> Multilingual Insights (HI, MR): PASSED")

if __name__ == "__main__":
    unittest.main()
