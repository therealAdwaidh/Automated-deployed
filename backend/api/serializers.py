from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'cleaned_text', 'predicted_score', 'created_at']
        read_only_fields = ['id', 'created_at']

class PredictionInputSerializer(serializers.Serializer):
    review_text = serializers.CharField(required=True, allow_blank=False)