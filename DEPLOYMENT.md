# Deployment Guide

## Frontend (Vercel)

### Setup:
1. Connect your GitHub repo to Vercel
2. Set Build Command: `cd frontend && npm install && npm run build`
3. Set Output Directory: `frontend/build`
4. Add Environment Variables in Vercel:
   - `REACT_APP_API_URL`: Set to your backend API URL (e.g., `https://your-backend.herokuapp.com/api`)

### Deploy:
```bash
git push origin main
```
Vercel will auto-deploy on push.

---

## Backend (Heroku or Similar)

### Prerequisites:
- Heroku CLI installed
- Python 3.9+
- Procfile and requirements.txt configured

### Setup Environment Variables:
Create a `.env` file in the `backend/` directory with:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=your-backend.herokuapp.com,localhost
CORS_ALLOWED_ORIGINS=https://automated-deployed.vercel.app,http://localhost:3000
```

### Create Heroku App:
```bash
cd backend
heroku login
heroku create your-app-name
```

### Set Environment Variables:
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-super-secret-key-change-this
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com,localhost
heroku config:set CORS_ALLOWED_ORIGINS=https://automated-deployed.vercel.app,http://localhost:3000
```

### Deploy:
```bash
git push heroku main  # or master depending on branch
```

### Run Migrations:
```bash
heroku run python manage.py migrate
```

### View Logs:
```bash
heroku logs --tail
```

---

## Important Notes:
- Replace `automated-deployed.vercel.app` with your actual Vercel domain
- Replace `your-backend.herokuapp.com/api` with your actual backend URL in Vercel env vars
- Ensure model files (`best_ml_model.pkl`, `best_ml_vectorizer.pkl`, `best_ml_svd.pkl`) are in the `models/` directory
- Commit all changes to GitHub before deploying
