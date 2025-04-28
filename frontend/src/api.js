// API configuration utility
import axios from 'axios';

// Use the environment variable in production, fallback to proxy setup in development
const baseURL = process.env.REACT_APP_API_URL || '';

const api = axios.create({
  baseURL
});

export default api;
