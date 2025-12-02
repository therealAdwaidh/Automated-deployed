import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ReviewPredictor.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const ReviewPredictor = ({ showOnlyForm, showOnlyHistory, allReviews, setAllReviews }) => {
  const [reviewText, setReviewText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [successMessage, setSuccessMessage] = useState(null);

  // Clear messages after 5 seconds
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!reviewText.trim()) {
      setError('Please enter a review');
      return;
    }

    if (reviewText.trim().length < 10) {
      setError('Review must be at least 10 characters long');
      return;
    }

    // Validate that input contains at least some actual words (letters)
    const hasLetters = /[a-zA-Z]/.test(reviewText);
    if (!hasLetters) {
      setError('Invalid input! Please enter a review with actual words. Numbers and symbols alone are not valid reviews.');
      return;
    }

    // Check if input is mostly numbers/symbols (less than 30% alphabetic characters)
    const letterCount = (reviewText.match(/[a-zA-Z]/g) || []).length;
    const totalCharacters = reviewText.trim().length;
    const letterPercentage = (letterCount / totalCharacters) * 100;

    if (letterPercentage < 30) {
      setError('Invalid input! Your review contains too many symbols or numbers. Please use mostly words.');
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);
    setSuccessMessage(null);

    try {
      const response = await axios.post(`${API_URL}/predict/`, {
        review_text: reviewText
      });

      if (response.data.success) {
        setPrediction(response.data.data);
        setReviewText('');
        setSuccessMessage('Review predicted successfully!');
        
        // Instantly add the new review to the list
        const newReview = {
          id: response.data.data.id,
          cleaned_text: response.data.data.cleaned_text,
          predicted_score: response.data.data.predicted_score,
          created_at: new Date().toISOString()
        };
        
        if (setAllReviews) {
          setAllReviews([newReview, ...allReviews]);
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Prediction failed. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRatingColor = (score) => {
    if (score >= 4) return '#4CAF50';
    if (score === 3) return '#FF9800';
    return '#f44336';
  };

  const getRatingEmoji = (score) => {
    const emojis = {
      1: '😞',
      2: '😕',
      3: '😐',
      4: '',
      5: '😍'
    };
    return emojis[score] || '😐';
  };

  const formatDate = (dateString) => {
    const options = { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className="container">
      {!showOnlyHistory && (
        <div className="prediction-card">
          <div className="form-header">
            <h2>Write Your Review</h2>
            
          </div>
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="review">
                Your Review ({reviewText.length}/500)
              </label>
              <textarea
                id="review"
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value.slice(0, 500))}
                placeholder="Share your honest feedback... (minimum 10 characters)"
                rows="6"
                disabled={loading}
                maxLength="500"
              />
            </div>

            <button 
              type="submit" 
              className="submit-btn"
              disabled={loading || !reviewText.trim() || reviewText.trim().length < 10}
            >
              {loading ? 'Predicting...' : 'Submit'}
            </button>
          </form>

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {successMessage && (
            <div style={{
              marginTop: '20px',
              padding: '15px',
              background: '#e8f5e9',
              borderLeft: '4px solid #4CAF50',
              borderRadius: '8px',
              color: '#2e7d32',
              animation: 'slideIn 0.3s ease-out'
            }}>
              {successMessage}
            </div>
          )}

          {prediction && (
            <div className="result-card">
              <h2>Prediction Result</h2>
              <div className="rating-display">
                <div className="rating-info">
                  <div 
                    className="rating-score"
                    style={{ color: getRatingColor(prediction.predicted_score) }}
                  >
                    {prediction.predicted_score} / 5
                  </div>
                  <div className="stars">
                    {[...Array(5)].map((_, i) => (
                      <span 
                        key={i} 
                        className={i < prediction.predicted_score ? 'star filled' : 'star'}
                      >
                        ★
                      </span>
                    ))}
                  </div>
                </div>
              </div>
              <div className="cleaned-text">
                <strong>Processed Text:</strong>
                <p>{prediction.cleaned_text}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {!showOnlyForm && (
        <div className="history-section">
          <button 
            className="history-toggle"
            onClick={() => setShowHistory(!showHistory)}
          >
            {showHistory ? 'Hide' : 'Show'} Review History ({allReviews.length})
          </button>

          {showHistory && (
            <div className="reviews-list">
              {allReviews.length === 0 ? (
                <p className="no-reviews">No reviews yet. Start by predicting your first review!</p>
              ) : (
                allReviews.map((review) => (
                  <div key={review.id} className="review-item">
                    <div className="review-header">
                      <span 
                        className="review-score"
                        style={{ backgroundColor: getRatingColor(review.predicted_score) }}
                      >
                        {review.predicted_score} ★
                      </span>
                      <span className="review-date">
                        {formatDate(review.created_at)}
                      </span>
                    </div>
                    <p className="review-text">{review.cleaned_text}</p>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ReviewPredictor;