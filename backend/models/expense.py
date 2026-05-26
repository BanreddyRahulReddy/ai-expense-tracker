from . import db
from datetime import datetime

# This is the "Expense" table in our database
# Every time a user adds an expense, a new row is created here

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Links to User table
    amount = db.Column(db.Float, nullable=False)              # How much was spent (e.g. 250.00)
    description = db.Column(db.String(200), nullable=False)   # What was bought (e.g. "lunch at cafe")
    category = db.Column(db.String(100), nullable=False)      # Auto-predicted: Food, Transport, etc.
    date = db.Column(db.DateTime, default=datetime.utcnow)    # When it was added

    def to_dict(self):
        # Converts a row into a dictionary so we can send it as JSON to React
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "category": self.category,
            "date": self.date.strftime("%Y-%m-%d %H:%M")
        }

    def __repr__(self):
        return f"<Expense {self.description} - {self.amount}>"