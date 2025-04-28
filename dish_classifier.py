import logging
from openai import OpenAI
import os
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

# Define dish categories
DISH_CATEGORIES = [
    "Wet Sabzi",      # E.g., Paneer Butter Masala, Aloo Matar
    "Dry Sabzi",      # E.g., Aloo Gobhi, Bhindi Fry
    "Dal",            # E.g., Dal Makhani, Toor Dal
    "Rice",           # E.g., Pulao, Biryani
    "Roti",           # E.g., Chapati, Naan
    "Paratha",        # E.g., Aloo Paratha, Methi Paratha
    "Non-Veg Curry",  # E.g., Butter Chicken, Fish Curry
    "Dessert",        # E.g., Gulab Jamun, Kheer
    "Chaat",          # E.g., Chole Bhature, Pani Puri
    "South Indian",   # E.g., Dosa, Idli, Vada, Uttapam
    "Breakfast"       # E.g., Poha, Upma
]

# Dictionary of pre-classified dishes to avoid API calls and ensure accuracy
KNOWN_DISHES = {
    "chole bhature": "Chaat",
    "paneer butter masala": "Wet Sabzi", 
    "butter chicken": "Non-Veg Curry",
    "dal makhani": "Dal",
    "palak paneer": "Wet Sabzi",
    "aloo gobi": "Dry Sabzi", 
    "biryani": "Rice",
    "samosa": "Chaat",
    "gulab jamun": "Dessert",
    "pani puri": "Chaat",
    "rajma chawal": "Dal",
    # South Indian dishes with accurate classifications
    "masala dosa": "South Indian",
    "plain dosa": "South Indian",
    "idli": "South Indian",
    "vada": "South Indian",
    "uttapam": "South Indian",
    "sambar": "Dal",
    "upma": "Breakfast",
    "poha": "Breakfast",
    "medu vada": "South Indian",
    "rava dosa": "South Indian",
    "pesarattu": "South Indian",
    "appam": "South Indian"
}

def classify_dish_type(dish_name, recipe=None):
    """
    Classify a dish into one of the predefined categories
    
    Args:
        dish_name (str): Name of the dish
        recipe (dict, optional): Recipe information if available
    
    Returns:
        str: Dish category
    """
    try:
        # First check if this is a well-known dish with a pre-defined classification
        dish_name_lower = dish_name.lower()
        if dish_name_lower in KNOWN_DISHES:
            logger.info(f"Using pre-defined classification for {dish_name}: {KNOWN_DISHES[dish_name_lower]}")
            return KNOWN_DISHES[dish_name_lower]
            
        # If not in known dishes, try rule-based classification
        dish_type = rule_based_classification(dish_name)
        if dish_type:
            logger.info(f"Rule-based classification for {dish_name}: {dish_type}")
            return dish_type
        
        # Detect non-vegetarian dishes based on ingredients
        if recipe and is_non_vegetarian(recipe):
            logger.info(f"Classified {dish_name} as Non-Veg Curry based on ingredients")
            return "Non-Veg Curry"
            
        # If that fails, use AI to classify
        if recipe:
            ingredients_text = ", ".join([f"{ing['name']} ({ing['quantity']})" 
                                         for ing in recipe["ingredients"]])
            dish_type = ai_based_classification(dish_name, ingredients_text)
            if dish_type:
                logger.info(f"AI classification for {dish_name} with ingredients: {dish_type}")
                return dish_type
        
        # Fallback to AI with just the dish name
        dish_type = ai_based_classification(dish_name)
        logger.info(f"AI classification for {dish_name}: {dish_type}")
        return dish_type
        
    except Exception as e:
        logger.error(f"Error classifying dish: {str(e)}")
        # Default classification if all else fails
        return "Wet Sabzi"
        
def rule_based_classification(dish_name):
    """Classify dish based on keywords in the name"""
    dish_name_lower = dish_name.lower()
    
    # Check for South Indian dishes first
    if any(word in dish_name_lower for word in ["dosa", "idli", "vada", "uttapam", "sambhar", "sambar", "appam", "pesarattu"]):
        return "South Indian"
    
    # Check for breakfast items
    if any(word in dish_name_lower for word in ["upma", "poha", "breakfast", "cereal", "porridge"]):
        return "Breakfast"
    
    # Check for other categories
    if any(word in dish_name_lower for word in ["dal", "daal", "lentil"]):
        return "Dal"
    elif any(word in dish_name_lower for word in ["rice", "pulao", "biryani", "fried rice"]):
        return "Rice"
    elif any(word in dish_name_lower for word in ["roti", "chapati", "phulka", "naan"]):
        return "Roti"
    elif any(word in dish_name_lower for word in ["paratha", "parantha"]):
        return "Paratha"
    elif "chole bhature" in dish_name_lower or "chana bhatura" in dish_name_lower:
        return "Chaat"
    elif any(word in dish_name_lower for word in ["chicken", "mutton", "fish", "prawn", "egg", "meat", "lamb"]):
        return "Non-Veg Curry"
    elif any(word in dish_name_lower for word in ["kheer", "halwa", "jamun", "barfi", "ladoo", "jalebi", "sweet"]):
        return "Dessert"
    elif any(word in dish_name_lower for word in ["chaat", "samosa", "tikki", "puri", "dahi"]):
        return "Chaat"
    elif any(word in dish_name_lower for word in ["masala", "curry", "makhani", "butter", "gravy"]):
        return "Wet Sabzi"
    elif any(word in dish_name_lower for word in ["fry", "dry", "sukhi", "roast"]):
        return "Dry Sabzi"
        
    return None

def is_non_vegetarian(recipe):
    """Check if recipe contains non-vegetarian ingredients"""
    non_veg_keywords = ["chicken", "mutton", "fish", "prawn", "shrimp", "egg", "meat", "lamb", "beef", "pork"]
    
    for ingredient in recipe.get("ingredients", []):
        ingredient_name = ingredient.get("name", "").lower()
        if any(keyword in ingredient_name for keyword in non_veg_keywords):
            return True
            
    return False

def ai_based_classification(dish_name, ingredients_text=None):
    """Use OpenAI to classify the dish"""
    try:
        # Prepare prompt
        if ingredients_text:
            prompt = f"""
            Classify the Indian dish "{dish_name}" with ingredients ({ingredients_text}) 
            into exactly one of these categories:
            {', '.join(DISH_CATEGORIES)}
            
            Pay special attention to South Indian dishes like dosas, idlis, and uttapams.
            Return only the category name, nothing else.
            """
        else:
            prompt = f"""
            Classify the Indian dish "{dish_name}" into exactly one of these categories:
            {', '.join(DISH_CATEGORIES)}
            
            Pay special attention to South Indian dishes like dosas, idlis, and uttapams.
            Return only the category name, nothing else.
            """
            
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies Indian dishes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Get the classification
        classification = response.choices[0].message.content.strip()
        
        # Validate classification
        if classification in DISH_CATEGORIES:
            return classification
        else:
            # Try to match with existing categories
            for category in DISH_CATEGORIES:
                if category.lower() in classification.lower():
                    return category
            
            # Special case for South Indian dishes
            if any(keyword in dish_name.lower() for keyword in ["dosa", "idli", "vada"]):
                return "South Indian"
            
            # Special case for Chole Bhature
            if "chole" in dish_name.lower() or "bhature" in dish_name.lower():
                return "Chaat"
            
            # Default to Wet Sabzi if no match
            return "Wet Sabzi"
            
    except Exception as e:
        logger.error(f"Error in AI classification: {str(e)}")
        return "Wet Sabzi"  # Default fallback
