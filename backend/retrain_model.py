"""
Retrain the model with correct feature dimensions matching the vectorizer
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Review
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from django.conf import settings
import numpy as np

print("=" * 80)
print("MODEL RETRAINING - FIXING FEATURE DIMENSION MISMATCH")
print("=" * 80)

# Get all reviews from database
reviews = Review.objects.all()

if reviews.count() == 0:
    print("\n❌ ERROR: No reviews in database to train on!")
    print("Please add some reviews first, then run this script.")
    print("=" * 80)
    exit()

# Extract texts and scores
texts = [review.cleaned_text for review in reviews]
scores = [review.predicted_score for review in reviews]

print(f"\n📊 Found {len(texts)} reviews for training")
print(f"Rating distribution: {dict(zip(*np.unique(scores, return_counts=True)))}")

# Create vectorizer with 200 max features (to match the model)
print("\n🔄 Creating TF-IDF vectorizer with 200 max features...")
vectorizer = TfidfVectorizer(
    max_features=200,
    ngram_range=(1, 2),
    max_df=0.95,
    min_df=1,
    lowercase=True,
    stop_words='english'
)

# Fit and transform
X = vectorizer.fit_transform(texts)
y = np.array(scores)

print(f"✓ Vectorizer fitted with shape: {X.shape}")

# Train the model
print("\n🤖 Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=4,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

print(f"✓ Model trained successfully")
print(f"  Classes: {model.classes_}")
print(f"  Features: {model.n_features_in_}")

# Save model and vectorizer to models folder
MODELS_DIR = os.path.join(settings.BASE_DIR.parent, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_ml_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'best_ml_vectorizer.pkl')

joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print(f"\n✅ Model saved to: {MODEL_PATH}")
print(f"✅ Vectorizer saved to: {VECTORIZER_PATH}")

print("\n" + "=" * 80)
print("RETRAINING COMPLETE - Testing predictions...")
print("=" * 80)

# Test predictions
test_reviews = [
    "This product is terrible and broken!",
    "Not satisfied with this purchase.",
    "It's okay, nothing special.",
    "Great product, very happy!",
    "Absolutely amazing! Best purchase ever!",
]

print()
for test_review in test_reviews:
    X_test = vectorizer.transform([test_review.lower()])
    pred = model.predict(X_test)[0]
    proba = model.predict_proba(X_test)[0]
    print(f"Review: '{test_review}'")
    print(f"  Prediction: {pred} stars")
    print(f"  Probabilities: {dict(zip(model.classes_, np.round(proba, 3)))}")
    print()

print("=" * 80)
