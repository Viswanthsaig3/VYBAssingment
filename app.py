from flask import Flask, request, jsonify
from nutrition_calculator import calculate_nutrition_for_dish
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>VYB Nutrition Calculator</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1 { color: #6d63ff; }
                form { margin: 20px 0; }
                input[type="text"] { padding: 10px; width: 70%; }
                input[type="submit"] { padding: 10px; background: #6d63ff; color: white; border: none; cursor: pointer; }
                input[type="submit"]:hover { background: #5a51d4; }
                .example { margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>VYB Nutrition Calculator</h1>
            <p>Enter an Indian dish name to get its nutritional information.</p>
            <form action="/calculate" method="post">
                <input type="text" name="dish_name" placeholder="Enter dish name (e.g. Paneer Butter Masala)">
                <input type="submit" value="Calculate">
            </form>
            <div class="example">
                <h3>Example Dishes:</h3>
                <ul>
                    <li>Paneer Butter Masala</li>
                    <li>Dal Makhani</li>
                    <li>Chole Bhature</li>
                    <li>Aloo Gobi</li>
                    <li>Butter Chicken</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.route("/calculate", methods=["POST"])
def calculate():
    dish_name = request.form.get("dish_name", "")
    if not dish_name:
        return jsonify({"error": "No dish name provided"}), 400
    
    try:
        result = calculate_nutrition_for_dish(dish_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error calculating nutrition: {str(e)}")
        return jsonify({"error": str(e), "dish_name": dish_name}), 500

@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json()
    if not data or "dish_name" not in data:
        return jsonify({"error": "No dish name provided"}), 400
    
    try:
        result = calculate_nutrition_for_dish(data["dish_name"])
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error calculating nutrition via API: {str(e)}")
        return jsonify({"error": str(e), "dish_name": data["dish_name"]}), 500

# Add compatibility endpoint for the /api/analyze-dish route that was causing 404 errors
@app.route("/api/analyze-dish", methods=["POST", "OPTIONS"])
def analyze_dish():
    # For OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        return "", 200
    
    # For POST requests
    data = request.get_json()
    if not data or "dish_name" not in data:
        return jsonify({"error": "No dish name provided"}), 400
    
    try:
        result = calculate_nutrition_for_dish(data["dish_name"])
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error analyzing dish: {str(e)}")
        return jsonify({"error": str(e), "dish_name": data["dish_name"]}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found. Available endpoints: /api/calculate, /api/analyze-dish"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
