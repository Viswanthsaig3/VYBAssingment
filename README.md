# NutriCalc AI

NutriCalc AI is a smart nutrition calculator specifically designed for Indian cuisine that helps you understand the nutritional content of your favorite dishes.

![NutriCalc AI Screenshot](https://i.imgur.com/sample-screenshot.png)

## What This App Does

NutriCalc AI takes the name of any Indian dish and:

1. **Finds a Recipe** - Automatically gets ingredient information
2. **Analyzes Ingredients** - Identifies quantities and matches ingredients to a nutrition database
3. **Calculates Nutrition** - Shows calories, protein, carbs, fat, and fiber per serving

## Key Features

- **Smart Dish Recognition** - Just enter any Indian dish name (like "Paneer Butter Masala" or "Dal Makhani")
- **Visual Dashboard** - See nutrition information in an easy-to-understand format
- **Ingredient Analysis** - View which ingredients contribute to the nutrition values
- **Export Options** - Download results as PDF or JSON
- **Supports All Indian Cuisine Types** - Works with North Indian, South Indian, and regional dishes

## How to Use

1. Type a dish name in the search box (or select from popular dishes)
2. Click "Calculate"
3. View the nutrition breakdown
4. Download or share the results

## Setup Instructions

### Prerequisites
- Python 3.7+
- Node.js and npm
- MongoDB
- OpenAI API key

### Quick Start
1. Clone the repository
2. Set up environment variables in `.env`:
   ```
   MONGO_URI=your_mongodb_connection_string
   OPENAI_API_KEY=your_openai_api_key
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
5. Run the application:
   ```bash
   python run.py
   ```
6. Open your browser at http://localhost:3000

## Deployment Information

The application is deployed and accessible at these URLs:

- **Frontend:** https://vybassingment-1.onrender.com/
- **Backend API:** https://vybassingment.onrender.com

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```
3. Create a `.env` file with required environment variables
4. Run the application:
   ```
   python run.py
   ```

## Environment Variables

- `MONGO_URI`: MongoDB connection string
- `OPENAI_API_KEY`: OpenAI API key for nutrition analysis
- `REACT_APP_API_URL`: Backend API URL (in production)

## Example Results

### Paneer Butter Masala
- **Calories**: 284.2 kcal
- **Protein**: 12.5g
- **Carbs**: 9.8g
- **Fat**: 21.3g
- **Fiber**: 2.1g

### Masala Dosa
- **Calories**: 180.0 kcal
- **Protein**: 5.0g
- **Carbs**: 30.0g
- **Fat**: 7.0g
- **Fiber**: 3.0g

## How It Works

The app uses a combination of AI and food science:

1. **OpenAI API** retrieves standard recipes for dishes
2. **Ingredient Processing** converts household measurements to grams
3. **Dish Classification** identifies the dish type to determine serving size
4. **Nutrition Database** provides values based on the Indian Food Composition Tables

## Technology Stack

- **Frontend**: React with styled-components
- **Backend**: Flask with Python
- **Data Processing**: Custom AI pipeline
- **Database**: MongoDB for ingredient nutrition data

## Limitations

- Nutrition values are estimates based on standard recipes
- Regional variations in cooking may affect actual nutritional content
- Some rare ingredients may not be in the database

---

Built with ❤️ to make nutrition science accessible for Indian cuisine
