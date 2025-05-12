from flask import Flask, render_template
from routes.home import home_bp
from routes.book import book_bp
from routes.review import review_bp
from routes.scoring import scoring_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(book_bp)
app.register_blueprint(review_bp)
app.register_blueprint(scoring_bp)

if __name__ == "__main__":
    app.run(debug=True)