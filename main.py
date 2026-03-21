import json
import os
import time
from data_fetch import get_gdelt_data
from processing import process_data
from map import create_map

# archivo cache
CACHE_FILE = "data.json"

# si ya existe, usarlo
if os.path.exists(CACHE_FILE):
    print("📦 Usando datos guardados...")
    with open(CACHE_FILE, "r") as f:
        articles = json.load(f)
else:
    print("🌐 Llamando a API...")
    articles = get_gdelt_data("protest")

    with open(CACHE_FILE, "w") as f:
        json.dump(articles, f)

# procesar
df = process_data(articles)

print(df.head())

# mapa
create_map(df)