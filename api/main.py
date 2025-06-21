from db import airports_collection, redis_geo, redis_popularity
from fastapi import FastAPI, HTTPException, Path, Body, Request
import re
from pydantic import BaseModel
from load_data import *
from typing import Optional
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Airport(BaseModel):
    name: str
    city: str
    iata_faa: Optional[str] = None
    icao: Optional[str] = None
    lat: float
    lng: float
    alt: int
    tz: str

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/airports")
def create_airport(airport: Airport):
    airport_dict = airport.dict()
    inserted = airports_collection.insert_one(airport_dict)
    codigo = airport.iata_faa or airport.icao
    if codigo:
        redis_geo.geoadd("airports-geo", (airport.lng, airport.lat, codigo))
    return {"id": str(inserted.inserted_id), "message": "Aeropuerto creado"}

@app.delete("/airports/{iata_code}")
def delete_airport(iata_code: str):
    pattern = re.compile(f"^{iata_code}$", re.IGNORECASE)
    airport = airports_collection.find_one(
        {"$or": [{"iata_faa": pattern}, {"icao": pattern}]}
    )
    if not airport:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    codigo = airport.get("iata_faa") or airport.get("icao")
    result = airports_collection.delete_one(
        {"$or": [{"iata_faa": pattern}, {"icao": pattern}]}
    )
    if codigo:
        redis_geo.zrem("airports-geo", codigo)
        redis_popularity.zrem("airports-popularity", codigo)
    return {"message": f"Aeropuerto '{codigo}' eliminado correctamente"}

@app.put("/airports/{iata_code}")
def update_airport(iata_code: str, update_data: dict = Body(...)):
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    pattern = re.compile(f"^{iata_code}$", re.IGNORECASE)
    result = airports_collection.update_one(
        {"$or": [{"iata_faa": pattern}, {"icao": pattern}]},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    codigo = update_data.get("iata_faa") or update_data.get("icao") or iata_code.upper()
    lat = update_data.get("lat")
    lng = update_data.get("lng")
    if lat is not None and lng is not None:
        redis_geo.geoadd("airports-geo", (lng, lat, codigo))
    return {"message": "Aeropuerto actualizado correctamente"}

@app.get("/airports")
def get_airports():
    airports = list(airports_collection.find({}, {"_id": 0}))
    return airports

@app.get("/airports/popular")
def get_popular_airports():
    codes = redis_popularity.zrevrange("airports-popularity", 0, 9)
    popular_airports = []

    for idx, code in enumerate(codes):
        pattern = re.compile(f"^{code}$", re.IGNORECASE)
        airport = airports_collection.find_one(
            {"$or": [{"iata_faa": pattern}, {"icao": pattern}]},
            {"_id": 0}
        )
        if airport:
            airport['position'] = idx + 1
            popular_airports.append(airport)
    
    return popular_airports


@app.get("/airports/nearby")
def get_nearby(lon: float, lat: float, radius: float):
    nearby = redis_geo.georadius("airports-geo", lon, lat, radius, "km")
    return nearby

@app.get("/airports/{iata_code}")
def get_airport(iata_code: str):
    pattern = re.compile(f"^{iata_code}$", re.IGNORECASE)
    airport = airports_collection.find_one(
        {"$or": [{"iata_faa": pattern}, {"icao": pattern}]},
        {"_id": 0}
    )
    if not airport:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    redis_popularity.zincrby("airports-popularity", 1, str(iata_code).upper())
    contador = len(redis_popularity.zrevrange("airports-popularity", 0, 10))
    if contador == 1:
        redis_popularity.expire("airports-popularity", 86400)
    return airport
