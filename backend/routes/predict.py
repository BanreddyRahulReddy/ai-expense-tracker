"""
predict.py

PURPOSE: ML-related API endpoints.

- POST /predict/category   → predict category from description text
- GET  /predict/forecast   → predict next month's spending
- GET  /predict/peers      → compare user spending vs dataset averages
"""

from flask import Blueprint, request, jsonify
from ml.classifier import predict_category
from ml.forecaster import forecast_next_month
from models.expense import Expense
from sqlalchemy import func
from models import db
from routes.auth import decode_token

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")

def get_user_id():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return decode_token(token)

@predict_bp.route("/category", methods=["POST"])
def category():
    data = request.get_json()
    description = data.get("description", "").strip()
    if not description:
        return jsonify({"error": "Description required"}), 400
    result = predict_category(description)
    return jsonify(result), 200

@predict_bp.route("/forecast", methods=["GET"])
def forecast():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    monthly = db.session.query(
        func.strftime("%Y-%m", Expense.date).label("month"),
        func.sum(Expense.amount).label("total")
    ).filter_by(user_id=user_id).group_by("month").order_by("month").all()
    if not monthly:
        return jsonify({"predicted": 0, "trend": "no data", "change_pct": 0}), 200
    totals = [round(float(r[1]), 2) for r in monthly]
    return jsonify(forecast_next_month(totals)), 200

# from flask import Blueprint, request, jsonify, session
# from ml.classifier import predict_category
# from ml.forecaster import forecast_next_month
# from models.expense import Expense
# from sqlalchemy import func
# from models import db
# import json, os

# predict_bp = Blueprint("predict", __name__, url_prefix="/predict")


# # ─── PREDICT CATEGORY ──────────────────────────────────────────────────────

# @predict_bp.route("/category", methods=["POST"])
# def category():
#     """
#     Called live as user types in the expense description box.
#     Expects: { "description": "netflix subscription" }
#     Returns: { "category": "Entertainment", "confidence": 94.2 }
#     """
#     data = request.get_json()
#     description = data.get("description", "").strip()

#     if not description:
#         return jsonify({"error": "Description required"}), 400

#     result = predict_category(description)
#     return jsonify(result), 200


# # ─── FORECAST NEXT MONTH ───────────────────────────────────────────────────

# @predict_bp.route("/forecast", methods=["GET"])
# def forecast():
#     """
#     Looks at user's last 6 months of spending.
#     Predicts what they'll spend next month.
#     """
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     # Get monthly totals (last 6 months)
#     monthly = db.session.query(
#         func.strftime("%Y-%m", Expense.date).label("month"),
#         func.sum(Expense.amount).label("total")
#     ).filter_by(user_id=user_id).group_by("month").order_by("month").all()

#     if not monthly:
#         return jsonify({"predicted": 0, "trend": "no data", "change_pct": 0}), 200

#     totals = [round(float(r[1]), 2) for r in monthly]
#     result = forecast_next_month(totals)
#     return jsonify(result), 200


# # ─── PEER COMPARISON ───────────────────────────────────────────────────────

# @predict_bp.route("/peers", methods=["GET"])
# def peers():
#     """
#     Compares user's category spending against dataset averages.
#     Returns a list like:
#     [
#       { "category": "Transport", "user_pct": 65, "peer_pct": 42 },
#       ...
#     ]
#     """
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     # Load peer averages computed from Kaggle dataset
#     avg_path = os.path.join(os.path.dirname(__file__), "../ml/peer_averages.json")
#     try:
#         with open(avg_path) as f:
#             peer_data = json.load(f)
#     except FileNotFoundError:
#         return jsonify({"error": "Peer data not available"}), 404

#     # Get how many of user's expenses fall in each category
#     user_expenses = Expense.query.filter_by(user_id=user_id).all()
#     total_count = len(user_expenses)

#     if total_count == 0:
#         return jsonify([]), 200

#     from collections import Counter
#     cat_counts = Counter(e.category for e in user_expenses)

#     comparison = []
#     for cat, peer_pct in peer_data.items():
#         if cat == "avg_monthly_expense":
#             continue
#         user_pct = round((cat_counts.get(cat, 0) / total_count) * 100, 1)
#         comparison.append({
#             "category": cat,
#             "user_pct": user_pct,
#             "peer_pct": peer_pct
#         })

#     return jsonify(comparison), 200