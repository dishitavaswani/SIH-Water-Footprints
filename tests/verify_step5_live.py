import sys
import httpx

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

cases = ["en", "hi", "mr", "gu", "xyz"]
print("=" * 70)
print(" FASTAPI MULTILINGUAL LIVE ENDPOINT VERIFICATION")
print("=" * 70)

for lang in cases:
    url = f"http://127.0.0.1:8000/footprint?item=rice&lang={lang}"
    resp = httpx.get(url)
    status = resp.status_code
    print(f"\nGET /footprint?item=rice&lang={lang}")
    print(f"Status Code: {status}")
    if status == 200:
        data = resp.json()
        print(f"  • Item Name          : {data['item']}")
        print(f"  • Total WF (Numeric) : {data['total_litres_per_kg']}")
        print(f"  • Green / Blue / Grey: {data['green_wf']} / {data['blue_wf']} / {data['grey_wf']}")
        print(f"  • Unit String        : {data['unit']}")
        print(f"  • Comparison         : {data['comparison']}")
        print(f"  • Language Code      : {data['lang']}")
    else:
        print(f"  • Detail             : {resp.json().get('detail')}")

print("\n" + "=" * 70)
