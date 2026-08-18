import json
import urllib.request

def test_live_server_search():
    url = "http://127.0.0.1:8000/footprint?item=apple&lang=en"
    print(f"Connecting to live server endpoint: {url}...")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            status = resp.getcode()
            body = resp.read().decode('utf-8')
            data = json.loads(body)
            print(f"Response Status Code : {status}")
            print(f"Returned Item Name   : {data.get('item')}")
            print(f"Description          : {data.get('description')}")
            print(f"Total Water Footprint: {data.get('total_litres_per_kg')} {data.get('unit')}")
            print(f"Green Water          : {data.get('green_water_litres')} L")
            print(f"Blue Water           : {data.get('blue_water_litres')} L")
            print(f"Grey Water           : {data.get('grey_water_litres')} L")
            print(f"Tip                  : {data.get('tip')}")
            print(" -> LIVE SERVER SEARCH VERIFICATION: SUCCESS")
    except Exception as e:
        print(f" -> LIVE SERVER SEARCH ERROR: {e}")

if __name__ == "__main__":
    test_live_server_search()
