"""
app.py

PURPOSE: This is the MAIN file that starts the Flask server.
         It ties everything together:
         - Creates the Flask app
         - Sets up the database
         - Registers all route blueprints
         - Starts the server

RUN THIS TO START BACKEND: python app.py
"""

from flask import Flask
from flask_cors import CORS
from models import db
from config import SECRET_KEY, DATABASE
from routes.auth import auth_bp
from routes.expenses import expenses_bp
from routes.predict import predict_bp
from routes.insights import insights_bp

# ─── Create Flask App ────────────────────────────────────────────────────────

app = Flask(__name__)
app.permanent_session_lifetime = 86400  # session lasts 24 hours

# Allow React frontend (running on port 3000) to call this backend
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Configuration
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True

# ─── Initialize Database ─────────────────────────────────────────────────────

db.init_app(app)

with app.app_context():
    db.create_all()   # Creates tables if they don't exist
    print("✅ Database ready.")

# ─── Register All Route Blueprints ───────────────────────────────────────────

# auth_bp  → handles /auth/register, /auth/login, /auth/logout
# expenses_bp → handles /expenses/add, /expenses/list, etc.
# predict_bp  → handles /predict/category, /predict/forecast, etc.
# insights_bp → handles /insights/tips

app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(insights_bp)


# ─── Health Check ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return {"status": "AI Expense Tracker API is running 🚀"}, 200


# ─── Start Server ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)