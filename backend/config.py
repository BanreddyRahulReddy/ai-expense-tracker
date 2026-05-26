import os
from dotenv import load_dotenv
 
# Load variables from .env file
load_dotenv()
 
# Secret key is used to protect user sessions (login security)
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey123")
 
# Path to our SQLite database file
DATABASE = os.path.join(os.path.dirname(__file__), "expenses.db")
 
# Gemini AI API key (for generating saving tips)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")