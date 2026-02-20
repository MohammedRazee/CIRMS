from flask import Blueprint, render_template, Flask, session
from bson import ObjectId
from routes.connection import mongo

book_bp = Blueprint("book", __name__)


@book_bp.route("/book/<book_id>", methods=["GET"])
def book(book_id):
    try:
        found_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
        find_review = mongo.db.reviews.find({"book_id": found_book["_id"]})
        find_review = list(find_review)

        score = found_book["score"]
        print(score)
        if found_book and find_review:
            print("Book found and review")

        print("Connection successful, searched book found.")
        return render_template(
            "book.html",
            title="book.name",
            book=found_book,
            review=find_review,
            score=score,
        )

    except Exception as e:
        print(f"Connection in book failed: {e}")
        return render_template(
            "book.html", title="Book", error="Unable to connect to the database."
        )
