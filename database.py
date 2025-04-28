import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
from fuzzywuzzy import fuzz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_nutrition_db_connection():
    """
    Connect to MongoDB and return database object
    
    Returns:
        pymongo.database.Database: MongoDB database object
    """
    try:
        # Get MongoDB connection string from environment variable
        mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://viswa:viswa@vybassingment.jtfa0ia.mongodb.net/?retryWrites=true&w=majority&appName=vybassingment")
        
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        
        # Test the connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Return the database
        return client["Food_Collection"]
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        raise

# Enhanced common name variations for Indian ingredients
INDIAN_INGREDIENT_VARIATIONS = {
    "tomato": ["tomatoes", "tamatar", "tomato puree", "tomato paste", "tomato sauce"],
    "tomatoes": ["tomato", "tamatar", "tomato puree", "tomato paste", "tomato sauce"],
    "onion": ["onions", "pyaaz", "onion chopped", "chopped onion", "sliced onion"],
    "onions": ["onion", "pyaaz", "onion chopped", "chopped onion", "sliced onion"],
    "potato": ["potatoes", "aloo", "aaloo"],
    "potatoes": ["potato", "aloo", "aaloo"],
    "chili": ["chilli", "chilies", "chillies", "mirch", "lal mirch", "green chili", "red chili"],
    "paneer": ["cottage cheese", "indian cheese", "panir"],
    "coriander": ["cilantro", "dhania", "coriander leaves", "fresh coriander"],
    "coriander powder": ["ground coriander", "dhaniya powder"],
    "cumin": ["jeera", "cumin seeds", "whole cumin"],
    "cumin powder": ["ground cumin", "jeera powder"],
    "turmeric": ["haldi", "turmeric powder"],
    "chickpeas": ["chole", "chana", "garbanzo", "kabuli chana"],
    "lentil": ["dal", "daal", "moong dal", "masoor dal", "toor dal", "chana dal"],
    "eggplant": ["brinjal", "aubergine", "baingan"],
    "okra": ["bhindi", "lady finger", "ladies finger"],
    "spinach": ["palak", "leafy greens"],
    "fenugreek": ["methi", "kasuri methi", "dried fenugreek"],
    "ginger-garlic paste": ["ginger garlic paste", "ginger and garlic paste", "garlic ginger paste"],
    "wheat flour": ["atta", "whole wheat flour", "chapati flour"],
    "all-purpose flour": ["maida", "refined flour", "white flour"],
    "vegetable oil": ["oil", "cooking oil", "refined oil", "sunflower oil"],
    "red kidney beans": ["rajma", "kidney beans"],
    "black gram": ["urad dal", "black lentils", "black dal"],
    "yogurt": ["curd", "dahi", "yoghurt", "yoghourt"],
    "green chili": ["green chilli", "hari mirch"]
}

def find_ingredient_in_db(db, ingredient_name):
    """
    Find an ingredient in the database
    
    Args:
        db (pymongo.database.Database): MongoDB database object
        ingredient_name (str): Name of the ingredient to find
    
    Returns:
        dict: Ingredient document from database or None if not found
    """
    try:
        # Normalize ingredient name
        ingredient_name = ingredient_name.lower().strip()
        
        # Try exact match on food_name
        result = db.nutrition_source.find_one({"food_name": {"$regex": f"^{ingredient_name}$", "$options": "i"}})
        if result:
            logger.info(f"Found exact match for {ingredient_name}")
            return result
            
        # Try partial match
        regex_pattern = f".*{ingredient_name}.*"
        result = db.nutrition_source.find_one({"food_name": {"$regex": regex_pattern, "$options": "i"}})
        if result:
            logger.info(f"Found partial match for {ingredient_name}: {result['food_name']}")
            return result
        
        # Try matching with common name variations (enhanced for Indian ingredients)
        common_variations = get_common_name_variations(ingredient_name)
        for variation in common_variations:
            result = db.nutrition_source.find_one({"food_name": {"$regex": f".*{variation}.*", "$options": "i"}})
            if result:
                logger.info(f"Found variation match for {ingredient_name} using {variation}: {result['food_name']}")
                return result
        
        # Try advanced fuzzy matching
        max_score = 0
        best_match = None
        
        # Threshold score for considering a match
        threshold = 80
        
        # Get all documents from the collection (consider adding pagination for large collections)
        cursor = db.nutrition_source.find({}, {"food_name": 1})
        
        for doc in cursor:
            if "food_name" in doc:
                score = fuzz.ratio(ingredient_name, doc["food_name"].lower())
                if score > max_score and score > threshold:
                    max_score = score
                    best_match = doc["food_name"]
        
        if best_match:
            result = db.nutrition_source.find_one({"food_name": best_match})
            logger.info(f"Found fuzzy match for {ingredient_name}: {best_match} (score: {max_score})")
            return result
            
        logger.warning(f"No match found for ingredient: {ingredient_name}")
        return None
    except Exception as e:
        logger.error(f"Error finding ingredient in database: {str(e)}")
        return None

def get_common_name_variations(ingredient_name):
    """Get common variations of ingredient names to improve matching"""
    variations = []
    
    # Handle common plural forms
    if ingredient_name.endswith('s'):
        variations.append(ingredient_name[:-1])  # Remove 's'
    else:
        variations.append(ingredient_name + 's')  # Add 's'
    
    # Check for Indian ingredient variations
    for standard_name, alternate_names in INDIAN_INGREDIENT_VARIATIONS.items():
        if ingredient_name == standard_name:
            variations.extend(alternate_names)
        elif ingredient_name in alternate_names:
            variations.append(standard_name)
            variations.extend([n for n in alternate_names if n != ingredient_name])
    
    # Remove parentheses and text within them
    clean_name = ingredient_name.split('(')[0].strip()
    if clean_name != ingredient_name:
        variations.append(clean_name)
    
    return variations
