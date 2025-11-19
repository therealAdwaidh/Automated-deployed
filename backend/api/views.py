from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, PredictionInputSerializer
import joblib
import os
from django.conf import settings
import re

# Load the trained model and vectorizer
MODEL_PATH = os.path.join(settings.BASE_DIR, 'best_model.pkl')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'best_ml_vectorizer.pkl')

model = None
vectorizer = None

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

try:
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Vectorizer loaded successfully!")
except Exception as e:
    print(f"Error loading vectorizer: {e}")
    vectorizer = None


def clean_text(text):
    """
    Clean the review text (customize based on your training preprocessing)
    This should match the cleaning done during model training
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


@api_view(['POST'])
def predict_rating(request):
    """
    Predict rating for a given review text
    """
    serializer = PredictionInputSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid input', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if model is None:
        return Response(
            {'error': 'Model not loaded. Please ensure best_model.pkl exists in the backend directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if vectorizer is None:
        return Response(
            {'error': 'Vectorizer not loaded. Please ensure best_ml_vectorizer.pkl exists in the backend directory.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    try:
        # Get the review text
        review_text = serializer.validated_data['review_text']
        
        # Clean the text
        cleaned_text = clean_text(review_text)
        
        # Vectorize the text
        vectorized_text = vectorizer.transform([cleaned_text])
        
        # If vectorizer produces more features than model expects, truncate to match
        expected_features = 200
        if vectorized_text.shape[1] > expected_features:
            vectorized_text = vectorized_text[:, :expected_features]
        
        # Make prediction
        prediction = model.predict(vectorized_text)[0]
        
        # Save to database
        review = Review.objects.create(
            cleaned_text=cleaned_text,
            predicted_score=int(prediction)
        )
        
        # Serialize and return
        response_serializer = ReviewSerializer(review)
        
        return Response(
            {
                'success': True,
                'data': response_serializer.data,
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