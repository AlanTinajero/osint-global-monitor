import requests
import time

def get_gdelt_data(keyword="protest"):
    time.sleep(5)

    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": keyword,
        "mode": "ArtList",
        "maxrecords": 10,
        "format": "json"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        print("Status:", response.status_code)

        if response.status_code != 200:
            print("❌ Error en API")
            print(response.text[:300])
            return []

        data = response.json()

        if "articles" not in data:
            print("⚠️ No hay artículos")
            return []

        return data["articles"]

    except Exception as e:
        print("❌ Error:", e)
        return []