# Review Rating Predictor - Full Stack Application

A full-stack web application that uses machine learning to predict ratings from user reviews. Built with React frontend and Django REST Framework backend.

## 🚀 Features

- **AI-Powered Predictions**: Uses a trained ML model to predict ratings (1-5 stars) from text reviews
- **Real-time Processing**: Instant predictions with visual feedback
- **Review History**: View all previous predictions with scores
- **Clean UI**: Modern, responsive interface with color-coded ratings
- **REST API**: Full-featured API for review predictions and data management

## 📋 Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- A trained ML model saved as `best_model.pkl`

## 🏗️ Project Structure

```
review-rating-app/
├── backend/                    # Django backend
│   ├── manage.py
│   ├── best_model.pkl         # Your trained ML model (required)
│   ├── requirements.txt
│   ├── config/                # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/                   # API application
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
└── frontend/                  # React frontend
    ├── package.json
    ├── public/
    └── src/
        ├── App.js
        ├── App.css
        ├── index.js
        ├── index.css
        └── components/
            ├── ReviewPredictor.js
            └── ReviewPredictor.css
```

## 🔧 Installation

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Place your ML model**
   - Copy your `best_model.pkl` file to the `backend/` directory
   - Ensure the model accepts text input and returns numeric scores (1-5)

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the backend server**
   ```bash
   python manage.py runserver
   ```
   Backend will run on: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal)
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Install additional packages**
   ```bash
   npm install axios
   ```

4. **Start the development server**
   ```bash
   npm start
   ```
   Frontend will run on: `http://localhost:3000`

## 🎯 Usage

1. **Open your browser** and navigate to `http://localhost:3000`

2. **Enter a review** in the text area

3. **Click "Predict Rating"** to get the AI prediction

4. **View results**:
   - Rating score (1-5 stars)
   - Visual representation with emojis and stars
   - Processed/cleaned text
   
5. **Check history** by clicking "Show Review History" to see all previous predictions

## 🔌 API Endpoints

### Base URL: `http://localhost:8000/api/`

#### 1. Predict Rating
- **Endpoint**: `POST /api/predict/`
- **Request Body**:
  ```json
  {
    "review_text": "This product is amazing!"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "cleaned_text": "this product is amazing",
      "predicted_score": 5,
      "created_at": "2025-11-19T10:30:00Z"
    },
    "message": "Prediction completed successfully"
  }
  ```

#### 2. Get All Reviews
- **Endpoint**: `GET /api/reviews/`
- **Response**:
  ```json
  {
    "success": true,
    "data": [...],
    "count": 10
  }
  ```

#### 3. Get Single Review
- **Endpoint**: `GET /api/reviews/<id>/`
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "cleaned_text": "...",
      "predicted_score": 5,
      "created_at": "..."
    }
  }
  ```

## 🧪 Testing the API

Using **curl**:

```bash
# Predict rating
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"review_text": "This product is absolutely amazing!"}'

# Get all reviews
curl http://localhost:8000/api/reviews/

# Get specific review
curl http://localhost:8000/api/reviews/1/
```

Using **Postman** or **Thunder Client**:
1. Create a POST request to `http://localhost:8000/api/predict/`
2. Set header: `Content-Type: application/json`
3. Add body: `{"review_text": "Your review here"}`

## 📊 Model Requirements

Your `best_model.pkl` must:

1. Be trained with scikit-learn
2. Be saved using `joblib.dump()`
3. Accept text input (string)
4. Return numeric predictions (1-5)

### Training Data Format
- **Feature**: `Cleaned_text` (preprocessed review text)
- **Target**: `Score` (rating from 1-5)


## ⚙️ Configuration

### Backend Configuration

Edit `backend/config/settings.py`:

```python
# Allow additional origins
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your production URL here
]

# Database (default: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Frontend Configuration

Edit `frontend/src/components/ReviewPredictor.js`:

```javascript
// Change API URL if backend runs on different port
const API_URL = 'http://localhost:8000/api';
```


**Port already in use:**
```bash
python manage.py runserver 8001  # Use different port
```

### Frontend Issues

**Module not found errors:**
```bash
npm install  # Reinstall dependencies
```

**Port 3000 already in use:**
```bash
PORT=3001 npm start  # Use different port
```

**API connection failed:**
- Ensure backend is running on port 8000
- Check API_URL in ReviewPredictor.js

## 📱 Admin Panel

Access Django admin at `http://localhost:8000/admin`

Features:
- View all reviews
- Filter by rating and date
- Search reviews
- Manage predictions

## 🚀 Deployment

### Backend (Django)

1. Set `DEBUG = False` in settings.py
2. Add your domain to `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Use gunicorn or uWSGI
5. Set up static files serving


## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.



## 🙏 Acknowledgments

- Built with Django REST Framework
- React for the frontend
- scikit-learn for machine learning

---

**Happy Predicting! 🎯**