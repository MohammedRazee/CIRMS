from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from bson import ObjectId
from routes.connection import mongo

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import string

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

        final_score = update_score(review_msg)
        mongo.db.reviews.insert_one({'book_id': ObjectId(book_id), 'name': name, 'email': email, 'review': review_msg, 'score': final_score})

        update_book_score(book_id)

        print("Connection successful in updating mongo")
        return redirect(url_for('book.book', book_id=book_id)) 
    
    except Exception as e:
        print(f"Error detected: {e}")
        return redirect(url_for('book.book', book_id=book_id))


@review_bp.route("/check-email", methods=['POST'])
def email_check():
    email = request.json.get('email')
    exists = mongo.db.reviews.find_one({'email': email})

    return jsonify({'exists': bool(exists)})


def update_score(rev):
    nltk.data.path.append('.venv/nltk_data')

    text = rev
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    cleaned_words = [word for word in words if word not in stop_words]
    
    text = ' '.join(cleaned_words)
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    return score['compound']

def update_book_score(book_id):
    pipeline = [
        {"$match": {"book_id": ObjectId(book_id)}},
        {"$group": {"_id": None, "avg": {"$avg": "$score"}}}
    ]
    score = list(mongo.db.reviews.aggregate(pipeline))
    final_score = score[0]['avg']
    mongo.db.books.update_one({'book_id': ObjectId(book_id)}, {'$set': { 'score': final_score}})