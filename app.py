from flask import Flask, render_template
from routes.home import home_bp
from routes.login import login_bp
from routes.book import book_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(book_bp)

if __name__ == "__main__":
    app.run(debug=True)