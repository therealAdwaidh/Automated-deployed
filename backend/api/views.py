from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, PredictionInputSerializer
import joblib
import os
from django.conf import settings
import re
import numpy as np

# Load the trained model, vectorizer, and SVD from models folder
MODELS_DIR = os.path.join(settings.BASE_DIR.parent, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_ml_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'best_ml_vectorizer.pkl')
SVD_PATH = os.path.join(MODELS_DIR, 'best_ml_svd.pkl')

model = None
vectorizer = None
svd = None

try:
    model = joblib.load(MODEL_PATH)
    print("ML model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

try:
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Vectorizer loaded successfully!")
except Exception as e:
    print(f"Error loading vectorizer: {e}")
    vectorizer = None

try:
    svd = joblib.load(SVD_PATH)
    print("SVD loaded successfully!")
except Exception as e:
    print(f"Error loading SVD: {e}")
    svd = None


def clean_text(text):
    """
    Clean the review text (customize based on your training preprocessing)
    This should match the cleaning done during model training
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


@api_view(['POST'])
def predict_rating(request):
    """
    Predict rating for a given review text using ML model with vectorizer and SVD
    """
    serializer = PredictionInputSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid input', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if model is None:
        return Response(
            {'error': 'Model not loaded. Please ensure best_ml_model.pkl exists in the models directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if vectorizer is None:
        return Response(
            {'error': 'Vectorizer not loaded. Please ensure best_ml_vectorizer.pkl exists in the models directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if svd is None:
        return Response(
            {'error': 'SVD not loaded. Please ensure best_ml_svd.pkl exists in the models directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    try:
        # Get the review text
        review_text = serializer.validated_data['review_text']
        
        # Clean the text
        cleaned_text = clean_text(review_text)
        
        # Vectorize the text
        vectorized_text = vectorizer.transform([cleaned_text])
        
        # Apply SVD transformation
        reduced_text = svd.transform(vectorized_text)
        
        # Make prediction with probability scores
        prediction = model.predict(reduced_text)[0]
        probabilities = model.predict_proba(reduced_text)[0]
        
        # Get the class with highest probability
        predicted_class = model.classes_[probabilities.argmax()]
        confidence = float(np.max(probabilities))
        
        # Save to database
        review = Review.objects.create(
            cleaned_text=cleaned_text,
            predicted_score=int(predicted_class)
        )
        
        # Serialize and return
        response_serializer = ReviewSerializer(review)
        
        return Response(
            {
                'success': True,
                'data': response_serializer.data,
                'confidence': confidence,
                'message': 'Prediction completed successfully'
            },
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        return Response(
            {'error': 'Prediction failed', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_all_reviews(request):
    """
    Get all reviews
    """
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(
        {
            'success': True,
            'data': serializer.data,
            'count': reviews.count()
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_review(request, pk):
    """
    Get a specific review by ID
    """
    try:
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Review.DoesNotExist:
        return Response(
            {'error': 'Review not found'},
            status=status.HTTP_404_NOT_FOUND
        )
