# ✈️ Aeropuertos App

Aplicación web para visualizar, agregar, modificar y eliminar aeropuertos, con funcionalidades geográficas para encontrar aeropuertos cercanos y mostrar los más populares.

## 📝 Descripción

Esta aplicación permite gestionar un catálogo de aeropuertos con la posibilidad de:

- Visualizar aeropuertos en un mapa interactivo.
- Consultar detalles completos de cada aeropuerto.
- Buscar **aeropuertos cercanos** a una ubicación.
- Consultar el **ranking de aeropuertos más populares**.
- Administrar el catálogo: **Agregar, modificar y eliminar aeropuertos**.

Los datos se almacenan en **MongoDB**, las ubicaciones se gestionan con **Redis GEO**, y la popularidad se mide con **Redis POPULARIDAD**.

Frontend desarrollado en **HTML + CSS + JS + Leaflet + MarkerCluster**.

## ⚙️ Tecnologías utilizadas

- **Backend:** Python, FastAPI
- **Base de datos:** MongoDB
- **Geolocalización & Popularidad:** Redis (GEO y POPULARIDAD)
- **Contenedores:** Docker, Docker Compose
- **Frontend:** HTML, CSS, JavaScript (Leaflet)
- **Dependencias principales:**
  - `fastapi`
  - `pymongo`
  - `redis`
  - `uvicorn`
  - `jinja2`

## 🚀 Funcionalidades principales

- 🗺️ **Mapa interactivo con clustering de marcadores.**
- 🔎 **Vista detalle** de cada aeropuerto.
- 📍 **Buscar aeropuertos cercanos** seleccionando radio (en km).
- ⭐ **Ranking de aeropuertos más populares.**
- ➕ **Agregar nuevos aeropuertos** desde formulario.
- ✏️ **Modificar aeropuertos existentes.**
- ❌ **Eliminar aeropuertos.**


## 🐳 Docker y contenedores

### Requisitos

- Tener instalado **Docker** y **Docker Compose**.

### Levantar la aplicación completa:

```bash
docker-compose up --build


## Visualización

- En esta ubicación vas a encontrar la página inicial en donde vas a poder navegar por las diferentes funcionalidades.

  ```
  localhost:8000
  ```
   

