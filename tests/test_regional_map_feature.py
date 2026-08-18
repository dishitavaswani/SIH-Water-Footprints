"""Test suite for Crop Suitability & Water Stress Map feature."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app
from database.regional_db import get_supported_regional_crops, get_regional_map_data, get_regional_detail

class TestRegionalMapFeature(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_regional_crops(self):
        """Test GET /regional/crops endpoint."""
        resp = self.client.get("/regional/crops")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(data["count"], 11)
        crop_ids = [c["crop_id"] for c in data["crops"]]
        self.assertIn("rice", crop_ids)
        self.assertIn("wheat", crop_ids)
        self.assertIn("jowar", crop_ids)
        self.assertIn("pearl_millet", crop_ids)
        print("\n -> GET /regional/crops: PASSED (11+ crops available)")

    def test_regional_map_data_suitability(self):
        """Test GET /regional/map-data with suitability layer."""
        resp = self.client.get("/regional/map-data?crop=rice&layer=suitability")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["crop_id"], "rice")
        self.assertEqual(data["layer"], "suitability")
        self.assertIn("PB", data["states"])
        self.assertIn("WB", data["states"])
        self.assertEqual(data["states"]["PB"]["category"], "unsuitable_high_stress")
        self.assertEqual(data["states"]["WB"]["category"], "highly_suitable")
        print(" -> GET /regional/map-data (Suitability): PASSED (PB unsuitable, WB highly suitable)")

    def test_regional_map_data_water_stress(self):
        """Test GET /regional/map-data with water_stress layer."""
        resp = self.client.get("/regional/map-data?crop=rice&layer=water_stress")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["layer"], "water_stress")
        self.assertEqual(data["states"]["PB"]["water_stress"], "severe")
        print(" -> GET /regional/map-data (Water Stress): PASSED (PB severe stress)")

    def test_regional_detail_punjab_rice(self):
        """Test GET /regional/detail for Rice in Punjab."""
        resp = self.client.get("/regional/detail?crop=rice&state=PB")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["crop"]["id"], "rice")
        self.assertEqual(data["region"]["id"], "PB")
        self.assertEqual(data["region"]["name"], "Punjab")
        self.assertIn("groundwater", data["analysis"]["why_explanation"].lower())
        self.assertIn("better_suited_alternatives", data["analysis"])
        self.assertIn("source", data["data_attribution"])
        print(" -> GET /regional/detail (Punjab Rice): PASSED")

    def test_regional_compare(self):
        """Test GET /regional/compare for Rice vs Jowar in Punjab."""
        resp = self.client.get("/regional/compare?crop_a=rice&crop_b=jowar&state=PB")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsNotNone(data["crop_a"])
        self.assertIsNotNone(data["crop_b"])
        self.assertEqual(data["crop_a"]["crop"]["id"], "rice")
        self.assertEqual(data["crop_b"]["crop"]["id"], "jowar")
        print(" -> GET /regional/compare: PASSED")

    def test_database_catalog_preserved(self):
        """Test GET /items still returns 41 catalog items intact."""
        resp = self.client.get("/items")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 41)
        print(" -> Preserved 41-item Database Catalog GET /items: PASSED")

if __name__ == "__main__":
    unittest.main()
