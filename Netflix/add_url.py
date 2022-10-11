from pymongo import MongoClient


client = MongoClient("mongodb://127.0.0.1:27017")
db = client.NetflixDB #select the database
shows = db.shows #select the collection

movie_pipeline = [
    {"$match": {"type" : "Movie"}}
]

for show in shows.aggregate(movie_pipeline):
    shows.update_one( { "_id" : show["_id"]},
        {   
            "$set" :{
                "url" : "/assets/images/movie_icon.png"
            }
        }
    )

tv_pipeline = [
    {"$match": {"type" : "TV Show"}}
]

for show in shows.aggregate(tv_pipeline):
    shows.update_one( { "_id" : show["_id"]},
        {   
            "$set" :{
                "url" : "/assets/images/TV_icon.png"
            }
        }
    )




