import React, { useState } from 'react';
import styled from 'styled-components';
import { HiOutlineFire, HiOutlineInformationCircle } from 'react-icons/hi';
import { Oval } from 'react-loader-spinner';
import api from '../utils/api'; // Import the API utility
import SearchForm from './SearchForm';
import NutritionResult from './NutritionResult';
import popularDishes from '../data/popularDishes';

const CalculatorWrapper = styled.div`
  display: grid;
  gap: 2rem;
  animation: fadeIn 0.5s ease forwards;
`;

const CalculatorContainer = styled.div`
  background: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
`;

const CalculatorHeader = styled.div`
  background: linear-gradient(to right, var(--secondary-light), var(--secondary-color));
  padding: 1.5rem;
  color: white;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
`;

const CalculatorContent = styled.div`
  padding: 1.5rem;

  @media (min-width: 768px) {
    padding: 2rem;
  }
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
  gap: 1rem;
  color: var(--text-secondary);
`;

const LoadingText = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  
  h4 {
    margin: 0;
    font-weight: 600;
    color: var(--primary-color);
  }
  
  p {
    margin: 0;
    font-size: 0.875rem;
    max-width: 250px;
    text-align: center;
    color: var(--text-tertiary);
  }
`;

const ErrorMessage = styled.div`
  color: var(--error-color);
  background-color: rgba(239, 68, 68, 0.1);
  padding: 1rem;
  border-radius: var(--border-radius);
  margin: 1rem 0;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;

  svg {
    flex-shrink: 0;
    margin-top: 0.25rem;
  }
`;

const PopularDishesSection = styled.div`
  margin-top: 1.5rem;
  background: var(--light-bg);
  padding: 1.25rem;
  border-radius: var(--border-radius);
`;

const SectionTitle = styled.h3`
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const DishesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.75rem;

  @media (min-width: 640px) {
    grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  }
`;

const DishTag = styled.button`
  background: white;
  border: 1px solid #e5e7eb;
  color: var(--text-color);
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  font-size: 0.875rem;
  transition: var(--transition-fast);
  font-weight: 500;
  text-align: center;
  line-height: 1.3;
  display: block;
  width: 100%;
  height: 100%;
  
  &:hover {
    background: var(--secondary-light);
    color: white;
    transform: none;
    border-color: var(--secondary-light);
    box-shadow: var(--shadow-sm);
  }
`;

const ResultsSection = styled.div`
  margin-top: 2rem;
  animation: slideUp 0.5s ease forwards;
`;

function NutritionCalculator() {
  const [dishName, setDishName] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loadingStage, setLoadingStage] = useState('');

  const calculateNutrition = async (dish) => {
    try {
      setLoading(true);
      setError('');
      setResult(null);
      
      // Show loading stages for better UX
      setLoadingStage('Fetching recipe ingredients...');
      await new Promise(r => setTimeout(r, 500)); // Small delay for UX
      
      setLoadingStage('Analyzing dish components...');
      const response = await api.post('/api/calculate', { dish_name: dish });
      
      setLoadingStage('Calculating nutritional values...');
      await new Promise(r => setTimeout(r, 500)); // Small delay for UX
      
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Unable to calculate nutrition. Please try a different dish.');
      console.error('Error calculating nutrition:', err);
    } finally {
      setLoading(false);
      setLoadingStage('');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!dishName.trim()) return;
    
    calculateNutrition(dishName);
  };

  const handlePopularDishClick = (dish) => {
    setDishName(dish);
    calculateNutrition(dish);
  };

  return (
    <CalculatorWrapper>
      <CalculatorContainer>
        <CalculatorHeader>
          <HiOutlineFire />
          Calculate Dish Nutrition
        </CalculatorHeader>
        
        <CalculatorContent>
          <SearchForm 
            dishName={dishName} 
            setDishName={setDishName} 
            handleSubmit={handleSubmit} 
            loading={loading}
          />

          {loading && (
            <LoadingContainer>
              <Oval
                height={60}
                width={60}
                color={`var(--secondary-color)`}
                secondaryColor="rgba(16, 185, 129, 0.2)"
                strokeWidth={3}
                strokeWidthSecondary={3}
                visible={true}
                ariaLabel='oval-loading'
              />
              <LoadingText>
                <h4>Analyzing Dish</h4>
                <p>{loadingStage}</p>
              </LoadingText>
            </LoadingContainer>
          )}
          
          {error && (
            <ErrorMessage>
              <HiOutlineInformationCircle size={18} />
              <span>{error}</span>
            </ErrorMessage>
          )}
          
          <PopularDishesSection>
            <SectionTitle>
              <HiOutlineFire size={16} />
              Popular Indian Dishes
            </SectionTitle>
            
            <DishesGrid>
              {popularDishes.slice(0, 12).map((dish, index) => (
                <DishTag 
                  key={index} 
                  onClick={() => handlePopularDishClick(dish)}
                  disabled={loading}
                >
                  {dish}
                </DishTag>
              ))}
            </DishesGrid>
          </PopularDishesSection>
        </CalculatorContent>
      </CalculatorContainer>

      {result && !loading && (
        <ResultsSection>
          <NutritionResult result={result} />
        </ResultsSection>
      )}
    </CalculatorWrapper>
  );
}

export default NutritionCalculator;
