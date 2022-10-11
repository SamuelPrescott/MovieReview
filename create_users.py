from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.NetflixDB
users = db.users

data = [
            {
                "name" : "Samuel Prescott",
                "username" : "sam",
                "password" : b"sam1",
                "email" : "sam@netflix.net",
                "admin" : True
             },
            {
                "name" : "George Clooney",
                "username" : "g-man",
                "password" : b"g-man1",
                "email" : "g-man@netflix.net",
                "admin" : False
            },
            {
                "name" : "Andy Samberg",
                "username" : "Jake",
                "password" : b"Jake1",
                "email" : "Jake.Peralta@netflix.net",
                "admin" : False
            },
            {
                "name" : "Emma Stone",
                "username" : "M&M",
                "password" : b"M&M1",
                "email" : "Emma.Stone@netflix.net",
                "admin" : False
            }
]
for new_user in data:
    new_user["password"] = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
    users.insert_one(new_user)