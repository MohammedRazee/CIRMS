from flask import Blueprint, render_template, Flask
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
