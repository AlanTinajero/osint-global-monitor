import pandas as pd

# coordenadas básicas por país
country_coords = {
    "USA": [37.0902, -95.7129],
    "Mexico": [23.6345, -102.5528],
    "France": [46.2276, 2.2137],
    "Turkey": [38.9637, 35.2433],
    "Brazil": [-14.2350, -51.9253],
    "India": [20.5937, 78.9629]
}

keywords = ["protest", "riot", "strike", "conflict", "violence"]

def process_data(articles):
    data = []

    for art in articles:
        text = art["title"].lower()
        country = art.get("sourcecountry", "Unknown")

        alert = any(word in text for word in keywords)

        coords = country_coords.get(country, [20, 0])

        data.append({
            "title": art["title"],
            "country": country,
            "url": art["url"],
            "alert": alert,
            "lat": coords[0],
            "lon": coords[1]
        })

    return pd.DataFrame(data)