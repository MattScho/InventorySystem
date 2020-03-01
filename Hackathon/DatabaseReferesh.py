from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

client = MongoClient()
client.drop_database("SmartHouse")

db = client["SmartHouse"]

loginCol = db["Logins"]
loginCol.insert({
    "userName": "admin",
    "hashedPassword": generate_password_hash("rootroot", method='sha256'),
    "ID": 1000000,
    "attempts": 0
})

adminCol = db["Admin"]
adminCol.insert({
    "ID": 1000000,
    "Name": "Alice"
})