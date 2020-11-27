from time import time
from pymongo import MongoClient

db = MongoClient("mongodb://localhost:27017")["cdn"]

db["zones"].update_many({}, {"$set": {"serial": str(int(time()))}})
