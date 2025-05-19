from flask import render_template, Blueprint, json, request, url_for, redirect, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from routes.connection import mongo


login_bp = Blueprint("login", __name__)

@login_bp.route("/register", methods=['GET'])
def register():
    print("Registration page opened")
    return render_template("register.html", title="Login Page")


@login_bp.route("/register", methods=['POST'])
def get_register():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        pwd = request.form.get('password')
        hashed_pwd = generate_password_hash(pwd)

        mongo.db.users.insert_one({'name': name, 'email': email, 'pwd': hashed_pwd})
        print("Successfully registered")
        return redirect(url_for('home.home'))
    
    except Exception as e:
        print(f"Registration error: {e}")
        return redirect(url_for('home.home'))
    
@login_bp.route("/login", methods=['GET'])
def login():
    print("Login page loaded")
    return render_template("login.html", title="Login Page")

@login_bp.route("/get_login", methods=['POST'])
def get_login():
    try:
        email = request.json.get('email')
        pwd = request.json.get('pwd')
        user = mongo.db.users.find_one({'email': email})
        if not user:
            return jsonify({'exists': bool(user), 'pass': False})
        
        if not check_password_hash(user['pwd'], pwd):
            return jsonify({'exists': False, 'pwd': True})
        
        session['username'] = user['name']
        session['email'] = user['email']
        print(session['username'])
        print("Logged in successfully")
        return jsonify({'success': True, 'redirect': url_for('home.home')})
    
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({'sucess': False,  'redirect': url_for('login.login')})
    
@login_bp.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home.home'))



