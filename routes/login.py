from flask import render_template, Blueprint, json, request
from werkzeug.security import generate_password_hash, check_password_hash
from routes.connection import mongo


login_bp = Blueprint("login", __name__)

@login_bp.route("/register", methods=['GET', 'POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    pwd = request.json.get('password')
    hashed_pwd = generate_password_hash(pwd)

    mongo.db.users.insert_one({'name': name, 'email': email, 'pwd': hashed_pwd})
    return render_template("register.html", title="Login Page")
