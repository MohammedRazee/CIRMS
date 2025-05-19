from flask import Flask, render_template, session
from routes.home import home_bp
from routes.book import book_bp
from routes.review import review_bp 
from routes.scoring import scoring_bp
from routes.login import login_bp


app = Flask(__name__)
app.secret_key = 'this-key-is-insanely-secret-damn'

app.register_blueprint(home_bp)
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)
app.register_blueprint(scoring_bp)
app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(debug=True)