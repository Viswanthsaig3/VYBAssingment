import React from 'react';
import './App.css';
import Header from './components/Header';
import NutritionCalculator from './components/NutritionCalculator';
import Footer from './components/Footer';
import ApiDebug from './components/ApiDebug';

function App() {
  // Only show debug component in development
  const isDev = process.env.NODE_ENV === 'development';
  
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <NutritionCalculator />
        {isDev && <ApiDebug />}
      </main>
      <Footer />
    </div>
  );
}

export default App;
