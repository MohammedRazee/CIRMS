from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Book"
mongo = PyMongo(app)