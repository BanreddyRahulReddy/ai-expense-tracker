from flask_sqlalchemy import SQLAlchemy

# This creates one shared database object used across all models
db = SQLAlchemy()

# Import models here so they are registered when app starts
from .user import User
from .expense import Expense