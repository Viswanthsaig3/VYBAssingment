import os
import json
from openai import OpenAI
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ValueError("OpenAI API key not found. Make sure OPENAI_API_KEY is set in the .env file.")

client = OpenAI(api_key=api_key)

def get_recipe_for_dish(dish_name):
    """
    Fetch recipe for a given dish using OpenAI API
    
    Args:
        dish_name (str): Name of the dish
    
    Returns:
        dict: Recipe with ingredients list
    """
    try:
        # Check if we have cached this recipe
        cache_file = f"cache/{dish_name.lower().replace(' ', '_')}.json"
        os.makedirs("cache", exist_ok=True)
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cached recipe: {str(e)}")
        
        # Prepare prompt for OpenAI
        prompt = f"""
        Give me the recipe for {dish_name}, a traditional Indian dish. 
        I only need the list of ingredients with approximate quantities in household measurements 
        (cups, tablespoons, teaspoons, etc.). Return the response as a JSON object with the following format:
        {{
            "dish_name": "{dish_name}",
            "ingredients": [
                {{"name": "ingredient name", "quantity": "quantity with unit"}},
                ...
            ]
        }}
        Only return the JSON data, no other text.
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Changed from gpt-4.1-nano to gpt-3.5-turbo which is widely available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides accurate Indian recipes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Process response
        recipe_text = response.choices[0].message.content.strip()
        # Clean up the response to ensure it's valid JSON
        recipe_text = recipe_text.replace("```json", "").replace("```", "").strip()
        
        recipe_data = json.loads(recipe_text)
        
        # Cache the recipe
        with open(cache_file, 'w') as f:
            json.dump(recipe_data, f)
        
        return recipe_data
    
    except Exception as e:
        logger.error(f"Error fetching recipe: {str(e)}")
        # Return a minimal structure in case of failure
        return {
            "dish_name": dish_name,
            "ingredients": [],
            "error": str(e)
        }
