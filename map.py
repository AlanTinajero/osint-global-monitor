import folium

def create_map(df):
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    for _, row in df.iterrows():
        if row["alert"]:
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row["title"],
            ).add_to(world_map)

    world_map.save("map.html")