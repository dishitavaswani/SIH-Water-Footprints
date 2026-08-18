import io
import sys
import json
import httpx
from PIL import Image, ImageDraw

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SERVER_URL = "http://127.0.0.1:8000/scan"

def create_non_food_image() -> io.BytesIO:
    """Generates a non-food geometric pattern image."""
    img = Image.new("RGB", (224, 224), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 200, 200], outline=(255, 255, 255), width=5)
    draw.line([0, 0, 224, 224], fill=(200, 200, 200), width=3)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

def create_unclear_blurry_image() -> io.BytesIO:
    """Generates a blurry, low-contrast image."""
    img = Image.new("RGB", (224, 224), color=(128, 128, 128))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

print("=" * 75)
print(" POST /scan ENDPOINT MANUAL RECOGNITION & DEFENSIVE VALIDATION TEST ")
print("=" * 75)

# 1. Test 5 Known Food Sample Images
known_samples = [
    ("Banana", "ml_model/sample_images/banana_sample.jpg"),
    ("Tomato", "ml_model/sample_images/tomato_sample.jpg"),
    ("Rice", "ml_model/sample_images/rice_sample.jpg"),
    ("Cucumber", "ml_model/sample_images/cucumber_sample.jpg"),
    ("Pineapple", "ml_model/sample_images/pineapple_sample.jpg"),
]

for label, file_path in known_samples:
    print(f"\n--- Testing Known Food Image: {label} ---")
    try:
        with open(file_path, "rb") as f:
            resp = httpx.post(f"{SERVER_URL}?lang=en", files={"file": (f"{label}.jpg", f, "image/jpeg")})
            print(f"Status Code: {resp.status_code}")
            d = resp.json()
            print(json.dumps(d, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error testing {label}: {e}")

# 2. Test Non-Food Image
print("\n--- Testing Non-Food Image (Geometric Pattern) ---")
non_food_buf = create_non_food_image()
resp = httpx.post(f"{SERVER_URL}?lang=en", files={"file": ("non_food.jpg", non_food_buf, "image/jpeg")})
print(f"Status Code: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

# 3. Test Unclear / Blurry Image
print("\n--- Testing Unclear / Blurry Image ---")
unclear_buf = create_unclear_blurry_image()
resp = httpx.post(f"{SERVER_URL}?lang=en", files={"file": ("unclear.jpg", unclear_buf, "image/jpeg")})
print(f"Status Code: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

# 4. Test Low-Confidence Multilingual Case (Hindi)
print("\n--- Testing Low-Confidence Multilingual Case (Hindi) ---")
unclear_buf_hi = create_unclear_blurry_image()
resp = httpx.post(f"{SERVER_URL}?lang=hi", files={"file": ("unclear_hi.jpg", unclear_buf_hi, "image/jpeg")})
print(f"Status Code: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

print("\n" + "=" * 75)
