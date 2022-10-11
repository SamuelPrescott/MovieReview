from typing import Any
from flask import Flask, json, request, jsonify, make_response
from pymongo import ALL, DESCENDING, MongoClient
import pymongo
from bson import ObjectId
import jwt
import datetime
from functools import wraps
import bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = 'jtown2021'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.NetflixDB # select database
shows = db.shows # select collection
users = db.users
blacklist = db.blacklist

# =-=-=-=-= Login and Admin Wrappers =-=-=-=-=

def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify( { 'message' : 'Token is Missing or Invalid' }), 401
        
        bl_token = blacklist.find_one({ "token" : token})
        if bl_token is not None:
            return make_response ( jsonify( { "message" : "Token has been terminated"}), 401)
        return func(*args, **kwargs)
    return jwt_required_wrapper

def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'])
        if data["admin"]:
            return func(*args, **kwargs)
        else:
            return make_response ( jsonify( { "message" : "Admin access is required"}), 401)   
    return admin_required_wrapper



#=-=-=-=-= handling adding, editing and deleting shows =-=-=-=-=# 

@app.route("/api/v1.0/shows", methods=["GET"])
def show_all_shows():
    page_num, page_size = 1, 6
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num -1))

    data_to_return = []
    for show in shows.find().skip(page_start).limit(page_size):
        show["_id"] = str (show["_id"])
        for review in show['reviews']:
            review["_id"] = str(review["_id"])
        data_to_return.append(show)

    return make_response(jsonify(data_to_return), 200)

@app.route("/api/v1.0/shows/<string:id>", methods=["GET"])
def show_one_show(id):
    show = shows.find_one({"_id":ObjectId(id)})
    if show is not None:
        show["_id"] = str(show["_id"])
        for review in show['reviews']:
            review["_id"] = str(review["_id"])

        return make_response(jsonify([show]), 200)
    else:
        return make_response(jsonify({"Error" : "Invalid Show ID"}), 404)


@app.route("/api/v1.0/shows", methods=["POST"])
# @jwt_required
def add_show():
    if "type" in request.form and "title" in request.form and "director" in request.form \
    and "cast" in request.form and "release_year" in request.form and "duration" in request.form \
            and "listed_in" in request.form and "description" in request.form and "url" in request.form:
            new_show = {
                "type": request.form["type"],
                "title": request.form["title"],
                "director": request.form["director"],
                "cast": request.form["cast"],
                "release_year": request.form["release_year"],
                "duration": request.form["duration"],
                "listed_in": request.form["listed_in"],
                "description": request.form["description"],
                "url": request.form["url"],
                "reviews": []
            }
            new_show_id = shows.insert_one(new_show)
            new_show_link = "http://localhost:5000/api/v1.0/shows/" + str(new_show_id.inserted_id)
            return make_response(jsonify({ "url" : new_show_link }), 201)
    else:
            return make_response(jsonify( { "Error" : "Missing form data" }), 404)

@app.route("/api/v1.0/shows/<string:id>", methods=["PUT"])
# @jwt_required
def edit_show(id):
    if "title" in request.form and "director" in request.form \
    and "cast" in request.form and "release_year" in request.form and "duration" in request.form \
            and "listed_in" in request.form and "description" in request.form and "url" in request.form:
            result = shows.update_one({"_id" : ObjectId(id)},
                {
                    "$set" : {
                        "title": request.form["title"],
                        "director": request.form["director"],
                        "cast": request.form["cast"],
                        "release_year": request.form["release_year"],
                        "duration": request.form["duration"],
                        "listed_in": request.form["listed_in"],
                        "description": request.form["description"],
                        "url": request.form["url"]
                    }
                }
            )
            if result.matched_count == 1:
                edit_show_link = "http://localhost:5000/api/v1.0/shows/" + id
                return make_response(jsonify({ "url" : edit_show_link}), 200)
            else:
                return make_response(jsonify({ "Error" : "Invalid Show ID"}), 404)
    else:
        return make_response(jsonify({"Error" : "Missing Form Data"}), 404)

#Pipeline function to return all Movies
@app.route("/api/v1.0/movies", methods=["GET"])
def search_movies():
    page_num, page_size = 1, 6
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num -1))


    # pipeline = [
    #     {"$match": {"type": "Movie"}},
    #     {"$sort": {
    #         "release_year": pymongo.DESCENDING}}
    # ]
    
    # 
    #             show["_id"] = str (show["_id"])
    # for show in shows.aggregate(pipeline):
    data_to_return = []
    for show in shows.find({"type" : "Movie"}).skip(page_start).limit(page_size).sort('release_year', DESCENDING):
        
        data_to_return.append({"url": show["url"], "_id": str(show["_id"]), "type": show["type"], "title": show["title"], "listed_in": show["listed_in"], "director": show["director"], "cast": show["cast"], "release_year": show["release_year"], "description": show["description"], "duration":show['duration']})
            
    return make_response(jsonify(data_to_return), 200)

#Pipeline to return all TV Shows
@app.route("/api/v1.0/TvShows", methods=["GET"])
def search_shows():
    page_num, page_size = 1, 6
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num -1))

    # pipeline = [
    #     {"$match": {"type": "TV Show"}},
    #     {"$sort": {
    #         "release_year": pymongo.DESCENDING}}
    # ]
    
        # show["_id"] = str (show["_id"])
        # for show in shows.aggregate(pipeline):        
    data_to_return = []
    for show in shows.find({"type" : "TV Show"}).skip(page_start).limit(page_size).sort('release_year', DESCENDING):
        
        data_to_return.append({"url": show["url"], "_id": str(show["_id"]), "type": show["type"], "title": show["title"], "listed_in": show["listed_in"], "director": show["director"], "cast": show["cast"], "release_year": show["release_year"], "description": show["description"], "duration":show['duration']})
            
    return make_response(jsonify(data_to_return), 200)


# @app.route("/api/v1.0/shows/<string:id>", methods=["DELETE"])
# @jwt_required
# @admin_required
# def delete_show(id):
#     result = shows.delete_one({"_id": ObjectId(id)})
#     if result.deleted_count == 1:
#         return make_response(jsonify({}), 200)
#     else:
#         return make_response(jsonify({ "Error" : "Invalid Show ID"}), 404)

@app.route("/api/v1.0/shows/<string:id>", methods=["DELETE"])
def delete_show(id):
    result = shows.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid show ID"}), 404)

# =-=-=-=-= Handling Reviews =-=-=-=

@app.route("/api/v1.0/shows/<string:id>/reviews", methods=["POST"])
# @jwt_required
def add_new_review(id):
    new_review = {
        "_id" : ObjectId(),
        "users_id": "61a78d95686d4188e83ae80a",
        "username": request.form["username"],
        "stars": request.form["stars"],
        "text": request.form["text"],
        "date": request.form["date"]
    }
    shows.update_one({"_id" : ObjectId(id)}, {"$push" : {"reviews" : new_review}})
    new_review_link = "http://localhost:5000/api/v1.0/shows/" + id + "/reviews/" + str(new_review["_id"])
    return make_response(jsonify({ "url" : new_review_link}), 201)


@app.route("/api/v1.0/shows/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    data_to_return = []
    show = shows.find_one( { "_id" : ObjectId(id)}, { "reviews" : 1, "_id" : 0 })
    for review in show["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)
    return make_response( jsonify( data_to_return), 200)
    


@app.route("/api/v1.0/shows/<string:sid>/reviews/<string:rid>", methods=["GET"])
def fetch_one_review(sid, rid):
    show = shows.find_one({"reviews._id": ObjectId(rid)},{"_id": 0, "reviews.$": 1})
    if show is None:
        return make_response(jsonify({"error": "Invalid show Id or review Id"}), 404)
    show['reviews'][0]["_id"] = str(show['reviews'][0]['_id'])
    return make_response(jsonify(show['reviews'][0]), 200)


@app.route("/api/v1.0/shows/<s_id>/reviews/<r_id>", methods=["PUT"])
def edit_review(s_id, r_id):
    edited_review = {
        "reviews.$.username": request.form["username"],
        "reviews.$.stars": request.form["stars"],
        "reviews.$.text": request.form["text"],
        "reviews.$.date": request.form["date"]
    }
    shows.update_one ( {"reviews._id" : ObjectId(r_id)}, {"$set" : edited_review })
    edit_review_url = "http://localhost:5000/api/v1.0/shows/" + s_id + "/reviews/" + r_id
    return make_response( jsonify( {"url":edit_review_url}), 200)

@app.route("/api/v1.0/shows/<s_id>/reviews/<r_id>", methods=["DELETE"])
def delete_review(s_id,r_id):
    shows.update_one({"_id" : ObjectId(s_id)}, {"$pull" : {"reviews" : { "_id" : ObjectId(r_id)}}})
    return make_response( jsonify( {} ), 204)


# Searching data
@app.route("/api/v1.0/shows/query", methods=["GET"])
def query_shows():
    pipeline = [
        {
        "$match": {"type": "Movie"}
        },
        {
            "$match" : {"listed_in" : "Comedies"}
        },
        {
            "$sort" : {"release_year" : pymongo.ASCENDING}
        },
    ]

    result = []
    for show in shows.aggregate(pipeline):
        result.append({'type':show["type"], 'title' :show['title'], 'listed_in': show['listed_in'], 'year':show['release_year']})

    return make_response(jsonify(result), 200)
    #
 


@app.route("/api/v1.0/login", methods=["GET"])
def login():
    auth = request.authorization
    if auth:
        user = users.find_one( { "username" : auth.username } )
        if user is not None:
            if bcrypt.checkpw( bytes( auth.password, 'UTF-8'), user["password"] ):
                token = jwt.encode( {
                        'user' : auth.username,
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                        'admin' : user["admin"]
                    }, app.config['SECRET_KEY'])
                return make_response(jsonify( { 'token' : token}), 200)
            else:
                return make_response(jsonify( { 'message' : "Bad Password"}), 401)
        else:
            return make_response(jsonify ( { "message" : "Bad username"}), 401)

    return make_response(jsonify( { "message" : "Authentication required"}), 401)

@app.route("/api/v1.0/logout", methods=["GET"])
@jwt_required
def logout():
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    if not token:
        return make_response(jsonify( { "message" : "Token is missing"}), 401)
    else:
        blacklist.insert_one( { "token" : token})
        return make_response(jsonify( { "message" : "Logout Successful"}), 200)

if __name__ == "__main__":
    app.run(debug=True)

