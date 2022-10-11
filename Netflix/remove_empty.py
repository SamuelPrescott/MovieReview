from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.NetflixDB #select the database
shows = db.shows #select the collection

for show in shows.find():
    shows.delete_many( { "_id" : show["_id"]},
        {
                'show.description' : ""
            
        }
    )