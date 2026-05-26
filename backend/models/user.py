from . import db
 
# This is the "User" table in our database
# Think of it like a blueprint for each user's row
 
class User(db.Model):
    __tablename__ = "users"
 
    id = db.Column(db.Integer, primary_key=True)          # Auto ID: 1, 2, 3...
    name = db.Column(db.String(100), nullable=False)       # User's full name
    email = db.Column(db.String(150), unique=True, nullable=False)  # Must be unique
    password_hash = db.Column(db.String(200), nullable=False)       # Encrypted password
 
    # One user can have many expenses (1-to-many relationship)
    expenses = db.relationship("Expense", backref="user", lazy=True)
 
    def __repr__(self):
        return f"<User {self.email}>"