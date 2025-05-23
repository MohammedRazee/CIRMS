from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
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
        if session['username']:
            rev = mongo.db.reviews.find_one({'book_id': ObjectId(book_id), 'email': session['email']})
            print(rev)
            if rev:
                return render_template("review.html", title="review_book.name", book=review_book , book_id=book_id, rev = rev)
        
        return render_template("review.html", title="review_book.name", book=review_book , book_id=book_id)

    
    except Exception as e:
        print(f"Connection fail: {e}")
        return render_template("review.html", title="review_book.name", book=review_book , book_id=book_id)


@review_bp.route("/submit/<book_id>", methods=['GET', 'POST'])
def submit(book_id):
    try:
        email = session['email']
        name = session['username']
        review_msg = request.form.get("re-review")

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
    book = request.json.get('check_book')
    exists = mongo.db.reviews.find_one({'email': email, 'book_id': ObjectId(book)})

    return jsonify({'exists': bool(exists)})

@review_bp.route('/re-review/<book_id>', methods=['GET', 'POST'])
def re_review(book_id):
    try:
        msg = request.form.get('re-review')

        score = update_score(msg)

        user = mongo.db.users.find_one({'name': session['username']})
        mongo.db.reviews.update_one({'email': user['email'], 'book_id': ObjectId(book_id)}, {'$set': {'score': score, 'edit': True, 'review': msg}})

        update_book_score(book_id)
        print("Book review updated")
        return redirect(url_for('home.dash'))
    
    except Exception as e:
        print(f"Re-review error: {e}")
        return redirect(url_for('home.dash'))



def update_score(rev):
    nltk.data.path.append('.venv/nltk_data')

    text = rev
    text = text.lower()

    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    cleaned_words = [word for word in words if word not in stop_words]
    
    text = ' '.join(cleaned_words)
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    scaled = 1 + ((score['compound'] + 1) / 2) * 4
    scaled = round(scaled, 1)
    return scaled

def update_book_score(book_id):
    pipeline = [
        {"$match": {"book_id": ObjectId(book_id)}},
        {"$group": {"_id": None, "avg": {"$avg": "$score"}}}
    ]
    score = list(mongo.db.reviews.aggregate(pipeline))
    final_score = score[0]['avg']
    final_score = round(final_score, 1)
    print(type(final_score))
    print(final_score)
    mongo.db.books.update_one({'_id': ObjectId(book_id)}, {'$set': { 'score': final_score}})
    print("Book score updated")