import pandas as pd
import requests
from io import StringIO

def get_fire_count(lat, lon, radius_km=10):
    """
    Get number of active fires in the radius around (lat, lon) in last 24h from NASA FIRMS.
    Default radius = 10km.
    """

    try:
        url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_Global_24h.csv"
        response = requests.get(url)

        if response.status_code != 200:
            print("NASA FIRMS fetch failed")
            return 0

        df = pd.read_csv(StringIO(response.text))

        # Haversine distance calculation
        from math import radians, sin, cos, sqrt, atan2

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth radius in km
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        df['distance'] = df.apply(lambda row: haversine(lat, lon, row['latitude'], row['longitude']), axis=1)

        count = df[df['distance'] <= radius_km].shape[0]
        return count

    except Exception as e:
        print("Fire history error:", e)
        return 0