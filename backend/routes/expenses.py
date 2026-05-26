"""
expenses.py

PURPOSE: All expense CRUD (Create, Read, Delete) operations.

- POST /expenses/add      → add a new expense (ML auto-categorizes it)
- GET  /expenses/list     → get all expenses for logged-in user
- DELETE /expenses/<id>   → delete a specific expense
- GET  /expenses/summary  → monthly totals grouped by category
"""

from flask import Blueprint, request, jsonify
from models import db
from models.expense import Expense
from ml.classifier import predict_category
from sqlalchemy import func
from routes.auth import decode_token

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

def get_user_id():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return decode_token(token)

@expenses_bp.route("/add", methods=["POST"])
def add_expense():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Please login first"}), 401
    data = request.get_json()
    amount = data.get("amount")
    description = data.get("description", "").strip()
    if not amount or not description:
        return jsonify({"error": "Amount and description are required"}), 400
    prediction = predict_category(description)
    category = data.get("category") or prediction["category"]
    expense = Expense(user_id=user_id, amount=float(amount), description=description, category=category)
    db.session.add(expense)
    db.session.commit()
    return jsonify({"message": "Expense added!", "expense": expense.to_dict(), "ml_prediction": prediction}), 201

@expenses_bp.route("/list", methods=["GET"])
def list_expenses():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Please login first"}), 401
    query = Expense.query.filter_by(user_id=user_id)
    category = request.args.get("category")
    if category:
        query = query.filter_by(category=category)
    expenses = query.order_by(Expense.date.desc()).all()
    return jsonify({"expenses": [e.to_dict() for e in expenses], "total": sum(e.amount for e in expenses)}), 200

@expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Please login first"}), 401
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200

@expenses_bp.route("/summary", methods=["GET"])
def summary():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Please login first"}), 401
    by_category = db.session.query(
        Expense.category, func.sum(Expense.amount).label("total")
    ).filter_by(user_id=user_id).group_by(Expense.category).all()
    by_month = db.session.query(
        func.strftime("%Y-%m", Expense.date).label("month"),
        func.sum(Expense.amount).label("total")
    ).filter_by(user_id=user_id).group_by("month").order_by("month").all()
    return jsonify({
        "by_category": [{"category": r[0], "total": round(r[1], 2)} for r in by_category],
        "by_month": [{"month": r[0], "total": round(r[1], 2)} for r in by_month]
    }), 200

# from flask import Blueprint, request, jsonify, session
# from models import db
# from models.expense import Expense
# from ml.classifier import predict_category
# from datetime import datetime
# from sqlalchemy import func

# expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


# def get_current_user_id():
#     """Helper: Get logged-in user's ID from session. Returns None if not logged in."""
#     return session.get("user_id")


# # ─── ADD EXPENSE ───────────────────────────────────────────────────────────

# @expenses_bp.route("/add", methods=["POST"])
# def add_expense():
#     """
#     Expects JSON: { "amount": 250, "description": "lunch at cafe" }
#     ML model auto-predicts the category.
#     User can also override category manually.
#     """

#     user_id = get_current_user_id()
#     if not user_id:
#         return jsonify({"error": "Please login first"}), 401

#     data = request.get_json()
#     amount = data.get("amount")
#     description = data.get("description", "").strip()

#     if not amount or not description:
#         return jsonify({"error": "Amount and description are required"}), 400

#     # Auto-predict category using ML model
#     prediction = predict_category(description)
#     # If user manually selected a category, use that instead
#     category = data.get("category") or prediction["category"]

#     expense = Expense(
#         user_id=user_id,
#         amount=float(amount),
#         description=description,
#         category=category
#     )

#     db.session.add(expense)
#     db.session.commit()

#     return jsonify({
#         "message": "Expense added!",
#         "expense": expense.to_dict(),
#         "ml_prediction": prediction   # Send back so UI can show confidence %
#     }), 201


# # ─── LIST ALL EXPENSES ─────────────────────────────────────────────────────

# @expenses_bp.route("/list", methods=["GET"])
# def list_expenses():
#     """
#     Returns all expenses for the logged-in user.
#     Optional filter: ?category=Food  or  ?month=2024-11
#     """

#     user_id = get_current_user_id()
#     if not user_id:
#         return jsonify({"error": "Please login first"}), 401

#     query = Expense.query.filter_by(user_id=user_id)

#     # Optional filters from URL query params
#     category = request.args.get("category")
#     month = request.args.get("month")   # format: "2024-11"

#     if category:
#         query = query.filter_by(category=category)

#     if month:
#         year, mon = month.split("-")
#         query = query.filter(
#             func.strftime("%Y", Expense.date) == year,
#             func.strftime("%m", Expense.date) == mon.zfill(2)
#         )

#     expenses = query.order_by(Expense.date.desc()).all()

#     return jsonify({
#         "expenses": [e.to_dict() for e in expenses],
#         "total": sum(e.amount for e in expenses)
#     }), 200


# # ─── DELETE EXPENSE ────────────────────────────────────────────────────────

# @expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
# def delete_expense(expense_id):
#     user_id = get_current_user_id()
#     if not user_id:
#         return jsonify({"error": "Please login first"}), 401

#     expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
#     if not expense:
#         return jsonify({"error": "Expense not found"}), 404

#     db.session.delete(expense)
#     db.session.commit()
#     return jsonify({"message": "Deleted successfully"}), 200


# # ─── SUMMARY (for charts) ──────────────────────────────────────────────────

# @expenses_bp.route("/summary", methods=["GET"])
# def summary():
#     """
#     Returns:
#     1. Total per category (for pie chart)
#     2. Total per month (for bar chart)
#     """

#     user_id = get_current_user_id()
#     if not user_id:
#         return jsonify({"error": "Please login first"}), 401

#     # Group by category
#     by_category = db.session.query(
#         Expense.category,
#         func.sum(Expense.amount).label("total")
#     ).filter_by(user_id=user_id).group_by(Expense.category).all()

#     # Group by month (last 6 months)
#     by_month = db.session.query(
#         func.strftime("%Y-%m", Expense.date).label("month"),
#         func.sum(Expense.amount).label("total")
#     ).filter_by(user_id=user_id).group_by("month").order_by("month").all()

#     return jsonify({
#         "by_category": [{"category": r[0], "total": round(r[1], 2)} for r in by_category],
#         "by_month": [{"month": r[0], "total": round(r[1], 2)} for r in by_month]
#     }), 200