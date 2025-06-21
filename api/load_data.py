import json
from db import *

with open("data/airports.json") as airports:
    datos = json.load(airports)

if airports_collection.count_documents({}) == 0:
    airports_collection.insert_many(datos)
    datos_cargados_mongo = airports_collection.count_documents({})
    print(f"La cantidad de datos cargados en mongo es {datos_cargados_mongo}")
else:
    "Datos ya cargados en mongo"


if redis_geo.zcard("airports-geo") > 0:
    print("Los datos ya fueron cargados en redis_geo")
else:
    try:
        for dato in datos:
            longitud = dato["lng"]
            latitud = dato["lat"]
            codigo = dato.get("iata_faa") or dato.get("icao")
            if codigo:
                redis_geo.geoadd("airports-geo", (longitud, latitud, codigo))
        datos_cargados_redis = redis_geo.zcard("airports-geo")
        print(f"La cantidad de datos cargados en airports-geo es {datos_cargados_redis}")
    except Exception as e:
        print(f"Error al cargar datos GEO en Redis: {e}")

