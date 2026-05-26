"""
insights.py

PURPOSE: Call Gemini AI API with user's spending summary
         and return 3 personalized saving tips.

- GET /insights/tips  → returns AI-generated advice
"""

from flask import Blueprint, request, jsonify
from models.expense import Expense
from models import db
from sqlalchemy import func
from routes.auth import decode_token
import os

insights_bp = Blueprint("insights", __name__, url_prefix="/insights")

def get_user_id():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return decode_token(token)

@insights_bp.route("/tips", methods=["GET"])
def get_tips():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    category_totals = db.session.query(
        Expense.category, func.sum(Expense.amount).label("total")
    ).filter_by(user_id=user_id).group_by(Expense.category).all()
    if not category_totals:
        return jsonify({"tips": ["Add some expenses first to get personalized tips!"]}), 200
    summary_lines = [f"{cat}: ${round(total, 2)}" for cat, total in category_totals]
    total_spend = sum(t[1] for t in category_totals)
    summary = "\n".join(summary_lines)
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
        prompt = f"""I am a university student. My monthly expenses:
{summary}
Total: ${round(total_spend, 2)}
Give me exactly 3 short practical money-saving tips. Format: 1. tip 2. tip 3. tip"""
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        tips = []
        for line in response.text.strip().split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                tips.append(line[2:].strip())
        return jsonify({"tips": tips[:3]}), 200
    except Exception as e:
        print(f"Gemini error: {e}")
        return jsonify({"tips": [
            "Track daily expenses to spot where money disappears.",
            "Set a monthly budget for your top spending category.",
            "Cook at home more often to reduce food expenses."
        ]}), 200

# from flask import Blueprint, jsonify, session
# from models.expense import Expense
# from models import db
# from sqlalchemy import func
# import google.generativeai as genai
# import os

# insights_bp = Blueprint("insights", __name__, url_prefix="/insights")

# # Set up Gemini API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))


# @insights_bp.route("/tips", methods=["GET"])
# def get_tips():
#     """
#     Builds a spending summary for the user and sends it to Gemini.
#     Returns 3 short, practical money-saving tips.
#     """

#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Not logged in"}), 401

#     # Get category-wise spending totals
#     category_totals = db.session.query(
#         Expense.category,
#         func.sum(Expense.amount).label("total")
#     ).filter_by(user_id=user_id).group_by(Expense.category).all()

#     if not category_totals:
#         return jsonify({"tips": ["Add some expenses first to get personalized tips!"]}), 200

#     # Build a readable summary string
#     summary_lines = [f"{cat}: ${round(total, 2)}" for cat, total in category_totals]
#     total_spend = sum(t[1] for t in category_totals)
#     summary = "\n".join(summary_lines)

#     # Build the prompt for Gemini
#     prompt = f"""
# I am a university student. Here is my monthly expense breakdown:

# {summary}

# Total: ${round(total_spend, 2)}

# Give me exactly 3 short, practical money-saving tips based on my spending.
# Format each tip on a new line starting with a number (1. 2. 3.).
# Keep each tip under 2 sentences. Be friendly and specific.
# """

#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(prompt)
#         tips_text = response.text.strip()

#         # Parse numbered tips into a list
#         tips = []
#         for line in tips_text.split("\n"):
#             line = line.strip()
#             if line and line[0].isdigit():
#                 # Remove leading "1. " etc.
#                 tip = line[2:].strip() if len(line) > 2 else line
#                 tips.append(tip)

#         if not tips:
#             tips = [tips_text]  # Fallback: return full response

#         return jsonify({"tips": tips[:3]}), 200

#     except Exception as e:
#         print(f"Gemini API error: {e}")
#         # Fallback tips if API fails or key not set
#         return jsonify({
#             "tips": [
#                 "Try to track daily expenses to spot where money disappears.",
#                 "Set a monthly budget for your top spending category.",
#                 "Cook at home more often to reduce food expenses."
#             ],
#             "note": "AI tips unavailable — showing default tips."
#         }), 200