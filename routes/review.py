from flask import Blueprint, render_template, Flask
from bson import ObjectId
from routes.connection import mongo

review_bp = Blueprint("review", __name__)

@review_bp.route("/review/<book_id>", methods=['GET'])
def review(book_id):
    try:
        review_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})

        return render_template("review.html", title="review_book.name", book=review_book , book_id=book_id)
    
    except Exception as e:
        print(f"Connection fail: {e}")
        return render_template("review.html", title="review_book.name", book=review_book , book_id=book_id)
