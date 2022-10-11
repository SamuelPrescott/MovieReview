from pymongo import MongoClient
import os
import pymongo
import bson
from pprint import pprint

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.NetflixDB
shows = db.shows


pipeline = [
    {
    "$match": {
        "type": "Movie"
        }
    },
    {
    "$match": {
        "listed_in" : "Comedies"
    }

    },  

{
    "$sort" : {
        "release_year" : pymongo.ASCENDING
    }
},
]

results = shows.aggregate(pipeline)

for show in results:
    print(" |Movie: {title}| |Cast: {first_castmember}| |Year: {year}|".format(
        type =show["type"],
        title=show["title"],
        first_castmember = show["cast"],
        year = show["release_year"],
    ))
