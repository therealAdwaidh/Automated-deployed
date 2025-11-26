"""
Test script to check model predictions on various reviews
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Review
from api.views import clean_text
import joblib
from django.conf import settings

# Load model and vectorizer from models folder
MODELS_DIR = os.path.join(settings.BASE_DIR.parent, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_ml_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'best_ml_vectorizer.pkl')

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("=" * 80)
print("MODEL PREDICTION TEST")
print("=" * 80)

# Test reviews with different sentiments
test_reviews = [
    ("This product is absolutely terrible and completely broke after one day.", "Very Negative"),
    ("Terrible quality, waste of money.", "Negative"),
    ("Not satisfied with this purchase at all.", "Negative"),
    ("It's okay, nothing special.", "Neutral"),
    ("Good product, decent quality.", "Positive"),
    ("Excellent product! Very satisfied with my purchase.", "Positive"),
    ("Absolutely amazing! Best purchase ever made!", "Very Positive"),
    ("Love it so much, highly recommend!", "Very Positive"),
    ("Perfect! Five stars!", "Very Positive"),
    ("Horrible experience, never buying again.", "Very Negative"),
    ("Outstanding quality and fast shipping!", "Very Positive"),
    ("Mediocre at best.", "Neutral"),
]

print("\nTesting predictions:\n")

for i, (review_text, sentiment) in enumerate(test_reviews, 1):
    # Clean text
    cleaned_text = clean_text(review_text)
    
    # Vectorize
    vectorized_text = vectorizer.transform([cleaned_text])
    
    # Truncate if needed
    expected_features = 200
    if vectorized_text.shape[1] > expected_features:
        vectorized_text = vectorized_text[:, :expected_features]
    
    # Get predictions
    prediction = model.predict(vectorized_text)[0]
    probabilities = model.predict_proba(vectorized_text)[0]
    predicted_class = model.classes_[probabilities.argmax()]
    
    print(f"{i}. [{sentiment}]")
    print(f"   Review: {review_text}")
    print(f"   Cleaned: {cleaned_text}")
    print(f"   Prediction: {prediction}")
    print(f"   Using predict_proba: {predicted_class}")
    print(f"   Probabilities: {dict(zip(model.classes_, probabilities))}")
    print(f"   Feature shape: {vectorized_text.shape}")
    print()

print("=" * 80)
print("CHECKING MODEL ATTRIBUTES:")
print("=" * 80)
print(f"Model type: {type(model)}")
print(f"Model classes: {model.classes_}")
print(f"Number of features used: {vectorizer.get_feature_names_out().shape[0]}")
print(f"Vectorizer max features: {vectorizer.max_features}")
print(f"Model n_features_in_: {model.n_features_in_}")
