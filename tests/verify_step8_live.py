import io
import sys
import httpx
from PIL import Image

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def make_img():
    img = Image.new("RGB", (64, 64), color="green")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

print("=" * 75)
print(" MULTILINGUAL IMAGE SCANNING ENDPOINT LIVE VERIFICATION")
print("=" * 75)

for lang in ["en", "hi", "mr", "gu", "xyz"]:
    buf = make_img()
    files = {"file": ("apple.jpg", buf, "image/jpeg")}
    url = f"http://127.0.0.1:8000/scan?lang={lang}"
    resp = httpx.post(url, files=files)
    print(f"\nPOST /scan?lang={lang} -> Status {resp.status_code}")
    if resp.status_code == 200:
        d = resp.json()
        print(f"  • Success            : {d.get('success')}")
        print(f"  • Item Display Name  : {d.get('item')}")
        print(f"  • Canonical Label    : {d.get('canonical_label')}")
        print(f"  • Numeric Confidence : {d.get('confidence')} (type: {type(d.get('confidence')).__name__})")
        print(f"  • Total WF (Numeric) : {d.get('total_litres_per_kg')} {d.get('unit')}")
        print(f"  • Comparison         : {d.get('comparison')}")
        print(f"  • Sustainability Tip : {d.get('tip')}")
    else:
        print(f"  • Error Detail       : {resp.json().get('detail')}")

print("\n" + "=" * 75)
