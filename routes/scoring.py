from flask import Blueprint, render_template
from routes.connection import mongo
from bson import ObjectId

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import string

scoring_bp = Blueprint("scoring", __name__)


@scoring_bp.route("/scoring", methods=["GET"])
def scoring_set():
    # books = mongo.db.books.find()
    # books = list(books)

    # for book in books:
    #     scaled = book['score']
    #     scaled = round(scaled, 1)
    #     print(scaled)
    #     mongo.db.books.update_one({'_id': ObjectId(book['_id'])}, {'$set': {'score': scaled}})

    return "Hello World"
