import React from 'react';
import styled from 'styled-components';
import { HiOutlineSearch, HiOutlineArrowRight } from 'react-icons/hi';

const Form = styled.form`
  margin-bottom: 1.5rem;
`;

const InputWrapper = styled.div`
  position: relative;
  display: flex;
  box-shadow: var(--shadow-sm);
  border-radius: var(--border-radius);
  transition: var(--transition-fast);
  
  &:focus-within {
    box-shadow: var(--shadow);
  }
`;

const Input = styled.input`
  width: 100%;
  padding: 1rem 1.25rem;
  padding-left: 3rem;
  border: 1px solid #e5e7eb;
  border-radius: var(--border-radius) 0 0 var(--border-radius);
  font-size: 1rem;
  transition: var(--transition-fast);
  border-right: none;
  
  &:focus {
    outline: none;
    border-color: var(--primary-light);
  }
`;

const InputIcon = styled.span`
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  pointer-events: none;
`;

const Button = styled.button`
  background: var(--primary-color);
  color: white;
  padding: 0 1.5rem;
  border: none;
  border-radius: 0 var(--border-radius) var(--border-radius) 0;
  font-weight: 500;
  font-size: 1rem;
  transition: var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  
  &:hover {
    background: var(--primary-dark);
  }
  
  &:disabled {
    background: var(--text-tertiary);
    cursor: not-allowed;
  }
  
  @media (max-width: 640px) {
    padding: 0 1rem;
    
    span {
      display: none;
    }
  }
`;

const HintLabel = styled.div`
  font-size: 0.875rem;
  color: var(--text-tertiary);
  margin-top: 0.5rem;
  line-height: 1.4;
`;

const ExamplesList = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
`;

const ExampleChip = styled.button`
  background: transparent;
  border: 1px solid var(--primary-light);
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: var(--border-radius-full);
  font-size: 0.75rem;
  transition: var(--transition-fast);
  font-weight: 500;
  
  &:hover {
    background: var(--primary-color);
    color: white;
    transform: none;
    box-shadow: none;
  }
`;

function SearchForm({ dishName, setDishName, handleSubmit, loading }) {
  // Example dish names that can be clicked to fill the search box
  const exampleDishes = ["Butter Chicken", "Dal Makhani", "Masala Dosa", "Chole Bhature"];
  
  const handleExampleClick = (dish) => {
    setDishName(dish);
  };
  
  return (
    <Form onSubmit={handleSubmit}>
      <InputWrapper>
        <InputIcon>
          <HiOutlineSearch size={18} />
        </InputIcon>
        <Input
          type="text"
          value={dishName}
          onChange={(e) => setDishName(e.target.value)}
          placeholder="Enter any Indian dish name..."
          disabled={loading}
          required
          autoFocus
        />
        <Button type="submit" disabled={loading || !dishName.trim()}>
          <span>Calculate</span>
          <HiOutlineArrowRight size={18} />
        </Button>
      </InputWrapper>
      
      <HintLabel>
        Try these examples:
        <ExamplesList>
          {exampleDishes.map((dish, index) => (
            <ExampleChip
              key={index}
              type="button"
              onClick={() => handleExampleClick(dish)}
              disabled={loading}
            >
              {dish}
            </ExampleChip>
          ))}
        </ExamplesList>
      </HintLabel>
    </Form>
  );
}

export default SearchForm;
