import { useState, useCallback } from 'react';
import axios from 'axios';

/**
 * Custom hook for nutrition data calculation
 * @returns {Object} - Nutrition calculation state and functions
 */
export function useNutrition() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loadingStage, setLoadingStage] = useState('');

  /**
   * Calculate nutrition for a specific dish
   * @param {string} dishName - Name of the dish to analyze
   * @returns {Promise<Object>} - Nutrition data
   */
  const calculateNutrition = useCallback(async (dishName) => {
    try {
      setLoading(true);
      setError('');
      setResult(null);
      
      // Show loading stages for better UX
      setLoadingStage('Fetching recipe ingredients...');
      await new Promise(r => setTimeout(r, 500)); 
      
      setLoadingStage('Analyzing dish components...');
      const response = await axios.post('/api/calculate', { dish_name: dishName });
      
      setLoadingStage('Calculating nutritional values...');
      await new Promise(r => setTimeout(r, 500));
      
      setResult(response.data);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.error || 
        'Unable to calculate nutrition. Please try a different dish.';
      setError(errorMessage);
      console.error('Error calculating nutrition:', err);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
      setLoadingStage('');
    }
  }, []);

  /**
   * Clear previous results
   */
  const clearResults = useCallback(() => {
    setResult(null);
    setError('');
  }, []);

  return {
    result,
    loading,
    error,
    loadingStage,
    calculateNutrition,
    clearResults
  };
}
