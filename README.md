# 💰 SpendSmart — AI Expense Tracker
> Full-stack expense tracker with ML auto-categorization (95.6% accuracy),
> spend forecasting, and Gemini AI saving tips.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![React](https://img.shields.io/badge/React-18-61DAFB)
![ML Accuracy](https://img.shields.io/badge/ML%20Accuracy-95.6%25-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features
- 🤖 ML auto-categorization — 95.6% accuracy (LinearSVC + TF-IDF)
- 📈 Next-month spend forecasting (Linear Regression)
- 💡 AI saving tips powered by Gemini API
- 📊 Interactive dashboard with charts (Recharts)
- 🔐 JWT authentication with 7-day token expiry
- 🚀 Deployed live on Render + Vercel

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React.js, Recharts, Axios |
| Backend | Python, Flask, SQLAlchemy |
| Database | SQLite |
| ML Model | scikit-learn (LinearSVC, TF-IDF) |
| AI API | Google Gemini |
| Auth | JWT (PyJWT) |
| Deploy | Render (backend), Vercel (frontend) |


## Local Setup

### Backend
cd backend
pip3 install -r requirements.txt
python3 ml/generate_dataset.py
python3 ml/train_classifier.py
python3 app.py

### Frontend
cd frontend
npm install
npm start

## ML Model Performance
- Algorithm: LinearSVC with TF-IDF vectorization
- Training samples: 746 across 9 categories
- Cross-validation accuracy: 95.6% (±0.9%)
- Hold-out test accuracy: 94.0%
- Live prediction latency: ~500ms (debounced)
