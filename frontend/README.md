# NutriCalc AI Frontend

## Environment Configuration

This React application uses environment variables for configuration:

- In development: Uses the proxy configuration in `package.json` to connect to the local backend at http://localhost:5000
- In production: Uses `REACT_APP_API_URL` from `.env.production` to connect to the deployed backend

## Available URLs

- Production site: https://vybassingment-1.onrender.com/
- Production API: https://vybassingment.onrender.com

## Usage

To use the API utility:

```javascript
import api from '../api';

// Example API call
const getNutritionData = async (dishName) => {
  try {
    const response = await api.post('/api/calculate', { dish_name: dishName });
    return response.data;
  } catch (error) {
    console.error('Error fetching nutrition data:', error);
    throw error;
  }
};
```
