"""
Create a compatible TF-IDF vectorizer with 5000 max features
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from django.conf import settings

print("=" * 80)
print("CREATING NEW VECTORIZER WITH 5000 MAX FEATURES")
print("=" * 80)

# Create vectorizer with 5000 features to match your trained model
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    max_df=0.95,
    min_df=1,
    lowercase=True,
    stop_words='english'
)

# Fit on dummy sentiment data to initialize the vocabulary
dummy_texts = [
    'good product excellent quality',
    'bad quality terrible experience',
    'amazing purchase love it',
    'terrible service awful',
    'love it best purchase ever',
    'hate it worst product',
    'excellent outstanding fantastic',
    'poor mediocre disappointing',
    'perfect five stars',
    'awful horrible never again',
    'fantastic highly recommend',
    'worst waste of money',
    'best purchase best decision',
    'terrible broken disappointing',
    'great satisfied happy customer',
    'bad not worth it',
    'amazing quality great service',
    'poor quality bad value',
    'excellent customer support',
    'terrible customer service bad support',
]

vectorizer.fit(dummy_texts)

MODELS_DIR = os.path.join(settings.BASE_DIR.parent, 'models')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'best_ml_vectorizer.pkl')

# Backup old vectorizer
old_path = VECTORIZER_PATH + '.bak'
if os.path.exists(VECTORIZER_PATH):
    import shutil
    shutil.copy(VECTORIZER_PATH, old_path)
    print(f"\n✓ Backed up old vectorizer to: {old_path}")

# Save new vectorizer
joblib.dump(vectorizer, VECTORIZER_PATH)

print(f"\n✅ NEW vectorizer created successfully!")
print(f"   Path: {VECTORIZER_PATH}")
print(f"   Max features: {vectorizer.max_features}")
print(f"   Learned features: {len(vectorizer.get_feature_names_out())}")
print(f"   Ngram range: {vectorizer.ngram_range}")

print("\n" + "=" * 80)
print("TESTING WITH NEW VECTORIZER")
print("=" * 80)

# Load the model from models folder
import os
from django.conf import settings
MODELS_DIR = os.path.join(settings.BASE_DIR.parent, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_ml_model.pkl')

try:
    import joblib
    model = joblib.load(MODEL_PATH)
    print(f"\n✓ Model loaded: {model}")
    print(f"  Model expects: {model.n_features_in_} features")
    print(f"  Vectorizer produces: {len(vectorizer.get_feature_names_out())} features")
    
    if model.n_features_in_ == len(vectorizer.get_feature_names_out()):
        print(f"\n✅ PERFECT MATCH! Vectorizer and model are now compatible!")
    else:
        print(f"\n⚠️  Mismatch: Model needs {model.n_features_in_}, vectorizer produces {len(vectorizer.get_feature_names_out())}")
        
except Exception as e:
    print(f"\n❌ Error loading model: {e}")

print("\n" + "=" * 80)
