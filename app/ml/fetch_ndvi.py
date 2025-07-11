import datetime
import requests
import json

CLIENT_ID = ""  # leave blank
CLIENT_SECRET = "PLAK9b3a7d631d0d4685b54e8b5f31d88225"

def get_sentinel_token():
    url = "https://services.sentinel-hub.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        # print("Sentinel auth error:", response.text)
        return None

def get_ndvi(lat, lon):
    token = get_sentinel_token()
    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                },
                "bbox": [lon - 0.01, lat - 0.01, lon + 0.01, lat + 0.01]
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": (datetime.date.today() - datetime.timedelta(days=10)).isoformat(),
                        "to": datetime.date.today().isoformat()
                    }
                }
            }]
        },
        "output": {
            "width": 50,
            "height": 50,
            "responses": [{"identifier": "default", "format": {"type": "image/tiff"}}]
        },
        "evalscript": """
            //VERSION=3
            function setup() {
                return {
                    input: ["B08", "B04"],
                    output: { bands: 1 }
                };
            }

            function evaluatePixel(sample) {
                let ndvi = index(sample.B08, sample.B04);
                return [ndvi];
            }
        """
    }

    url = "https://services.sentinel-hub.com/api/v1/process"
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return 0.75  # placeholder NDVI value
    else:
        # print("NDVI fetch failed:", response.text)
        return None