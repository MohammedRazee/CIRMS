from flask import Blueprint, render_template, Flask, session, redirect, url_for
from bson import ObjectId
from routes.connection import mongo
import traceback

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=['GET'])
def home():
    try:
        books = mongo.db.books.find()
        book_list = []

        for book in books:
            book['_id'] = str(book['_id'])
            book_list.append(book)

        print("Connection successful, books found.")
        return render_template("index.html", title="Home Page", books=book_list)
    
    except Exception as e:
        print(f"Connection failed: {e}")
        traceback.print_exc()
        return render_template("index.html", title="Home Page", error="Unable to connect to the database.")
    
@home_bp.route("/dash", methods=['GET'])
def dash():
    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    email = user['email']
    books = []

    revs = mongo.db.reviews.find({'email': email})
    revs = list(revs)
    for rev in revs:
        book = mongo.db.books.find_one({'_id': ObjectId(rev['book_id'])})
        # book['_id'] = str(book['_id'])
        books.append(book)

    return render_template("dash.html", title=session['username'], books = books, reviews = revs)
