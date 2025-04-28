# Deploying to Render

## Prerequisites
- Create a Render account at [render.com](https://render.com)
- Push your code to a GitHub repository

## Deployment Steps

### 1. Backend Deployment
1. On Render dashboard, click "New" and select "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - Name: `nutriCalc-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Add the following environment variables:
     - `MONGO_URI`: Your MongoDB connection string
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `FLASK_ENV`: `production`

### 2. Frontend Deployment
1. On Render dashboard, click "New" and select "Static Site"
2. Connect your GitHub repository
3. Configure the service:
   - Name: `nutriCalc-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`
   - Add environment variable:
     - `REACT_APP_API_URL`: `https://vybassingment.onrender.com`

### 3. Update API URL in Frontend
Update your API requests to use the environment variable:

```js
// in frontend/src/hooks/useNutrition.js or relevant file
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
const response = await axios.post(`${API_URL}/api/calculate`, { dish_name: dishName });
```
