"""
train_classifier.py

Trains the expense category classifier using the generated dataset.
Run: python3 ml/train_classifier.py
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib, os, json

# ── Load generated training data ─────────────────────────────────────────────

csv_path = os.path.join(os.path.dirname(__file__), "../data/classifier_training.csv")

if not os.path.exists(csv_path):
    print(" classifier_training.csv not found.")
    print("   Run this first: python3 ml/generate_dataset.py")
    exit(1)

df = pd.read_csv(csv_path)
df.dropna(inplace=True)
df["description"] = df["description"].str.strip().str.lower()
df["category"]    = df["category"].str.strip().str.lower()

print(f"Loaded {len(df)} training samples")
print(f"Categories: {df['category'].value_counts().to_dict()}\n")

X = df["description"]
y = df["category"]

# ── Train model ───────────────────────────────────────────────────────────────

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 3),
        sublinear_tf=True,
        min_df=1,
    )),
    ("clf", LinearSVC(C=1.0, dual=True, max_iter=3000))
])

# 5-fold cross validation
cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(f"Cross-Validation Accuracy: {cv_scores.mean()*100:.1f}% (±{cv_scores.std()*100:.1f}%)")
print(f"   Per fold: {[f'{s*100:.1f}%' for s in cv_scores]}")

# Hold-out test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"\nHold-out Accuracy: {accuracy_score(y_test, y_pred)*100:.1f}%")
print(classification_report(y_test, y_pred, zero_division=0))

# Retrain on full data before saving
model.fit(X, y)

# ── Save model + categories ───────────────────────────────────────────────────

save_path = os.path.join(os.path.dirname(__file__), "model.pkl")
joblib.dump(model, save_path)
print(f"Model saved: {save_path}")

categories = sorted(df["category"].unique().tolist())
with open(os.path.join(os.path.dirname(__file__), "categories.json"), "w") as f:
    json.dump(categories, f, indent=2)

# ── Live prediction test ──────────────────────────────────────────────────────

print("\nLive prediction test:")
tests = [
    ("zomato food delivery",       "food"),
    ("uber cab ride",              "transport"),
    ("netflix subscription",       "entertainment"),
    ("amazon online shopping",     "shopping"),
    ("college tuition fee",        "education"),
    ("electricity bill payment",   "utilities"),
    ("laptop purchase amazon",     "technology"),
    ("doctor clinic consultation", "health"),
    ("flight ticket goa trip",     "travel"),
]
correct = 0
for desc, expected in tests:
    pred = model.predict([desc])[0]
    ok = pred == expected
    if ok: correct += 1
    print(f"  {'✅' if ok else '❌'} '{desc}' → {pred} (expected: {expected})")
print(f"\n  Score: {correct}/{len(tests)} = {correct/len(tests)*100:.0f}%")

# ── Peer averages fallback ────────────────────────────────────────────────────

avg_path = os.path.join(os.path.dirname(__file__), "peer_averages.json")
if not os.path.exists(avg_path):
    with open(avg_path, "w") as f:
        json.dump({"avg_monthly_expense": 214.95}, f)

print("\nDone! Now run: python3 app.py")