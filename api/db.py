from pymongo import MongoClient
import redis
import os

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["airport_db"]
airports_collection = db["airports"]

# Redis GEO
REDIS_GEO_HOST = os.getenv("REDIS_GEO_HOST", "localhost")
REDIS_GEO_PORT = int(os.getenv("REDIS_GEO_PORT", 6378))
redis_geo = redis.Redis(host=REDIS_GEO_HOST, port=REDIS_GEO_PORT, decode_responses=True)

# Redis Popularidad
REDIS_POP_HOST = os.getenv("REDIS_POP_HOST", "localhost")
REDIS_POP_PORT = int(os.getenv("REDIS_POP_PORT", 6377))
redis_popularity = redis.Redis(host=REDIS_POP_HOST, port=REDIS_POP_PORT, decode_responses=True)

print("Conexiones listas a MongoDB y Redis")
