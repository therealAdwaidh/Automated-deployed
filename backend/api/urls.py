from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_rating, name='predict_rating'),
    path('reviews/', views.get_all_reviews, name='get_all_reviews'),
    path('reviews/<int:pk>/', views.get_review, name='get_review'),
]