from django.db import models

class Review(models.Model):
    cleaned_text = models.TextField()
    predicted_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review {self.id} - Score: {self.predicted_score}"