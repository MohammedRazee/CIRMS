from flask import Blueprint, render_template, request, jsonify, redirect, url_for
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


@review_bp.route("/submit/<book_id>", methods=['GET', 'POST'])
def submit(book_id):
    try:
        email = request.form.get("email")
        name = request.form.get("name")
        review_msg = request.form.get("review")
        
        mongo.db.reviews.insert_one({'book_id': book_id, 'name': name, 'email': email, 'review': review_msg})
        print("Connection successful in updating mongo")
        return redirect(url_for('book.book', book_id=book_id)) 
    
    except Exception as e:
        print(f"Error detected: {e}")
        return redirect(url_for('book.book', book_id=book_id))


@review_bp.route("/check-email", methods=['POST'])
def email_check():
    email = request.json.get('email')
    exists = mongo.db.reviews.find_one({'email': email})
    print(bool(exists))
    return jsonify({'exists': bool(exists)})
