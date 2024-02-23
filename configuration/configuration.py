from pymongo import MongoClient

def get_database_airqualityserbia():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['AirQuality']
    collection = db['AirQualitySerbia']
    return collection