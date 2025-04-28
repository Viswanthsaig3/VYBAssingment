import React from 'react';
import './App.css';
import Header from './components/Header';
import NutritionCalculator from './components/NutritionCalculator';
import Footer from './components/Footer';

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <NutritionCalculator />
      </main>
      <Footer />
    </div>
  );
}

export default App;
