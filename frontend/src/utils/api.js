import axios from 'axios';

// Use backend URL from environment variable in production or fallback to relative URL in development
const API_URL = process.env.REACT_APP_API_URL || '';

// Create axios instance with the base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add response interceptor for debugging
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response || error);
    return Promise.reject(error);
  }
);

export default api;
