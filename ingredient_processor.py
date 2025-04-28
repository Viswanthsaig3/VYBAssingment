import re
import logging
from fuzzywuzzy import process
from database import find_ingredient_in_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced household measurement conversion to grams
HOUSEHOLD_MEASURES = {
    "cup": {
        "liquid": 240,
        "rice": 180,
        "flour": 125,
        "sugar": 200,
        "chickpeas": 200,
        "lentil": 200,
        "yogurt": 245,
        "dal": 200,
        "rajma": 200,
        "default": 150
    },
    "tablespoon": {
        "oil": 14,
        "ghee": 14,
        "liquid": 15,
        "spice": 8,
        "flour": 10,
        "sugar": 12,
        "default": 15
    },
    "teaspoon": {
        "spice": 5,
        "salt": 6,
        "powder": 3,
        "default": 5
    },
    "katori": {
        "default": 180
    },
    "glass": {
        "default": 240
    },
    "piece": {
        "onion": {
            "large": 150,
            "medium": 110,
            "small": 70,
            "default": 110
        },
        "tomato": {
            "large": 180,
            "medium": 120,
            "small": 80,
            "default": 120
        },
        "potato": {
            "large": 200,
            "medium": 150,
            "small": 100,
            "default": 150
        },
        "roti": 40,
        "bread": 30,
        "bhature": 60,
        "default": 50
    },
    "leaf": {
        "curry leaf": 0.5,  # A curry leaf weighs ~0.5g
        "default": 0.5
    },
    "leaves": {
        "curry leaves": 0.5,  # Multiple leaves - weight per leaf
        "default": 0.5
    },
    "inch": {
        "ginger": 15,  # 1 inch of ginger is ~15g
        "default": 10
    }
}

# Expanded ingredient categories to help with conversions
INGREDIENT_CATEGORIES = {
    "liquid": ["water", "milk", "curd", "yogurt", "oil", "ghee", "cream", "buttermilk", "coconut milk"],
    "spice": ["salt", "pepper", "cumin", "coriander", "turmeric", "chili", "garam masala", 
              "cardamom", "cinnamon", "clove", "mustard", "masala", "powder"],
    "vegetable": ["onion", "tomato", "potato", "carrot", "spinach", "cabbage", "cauliflower", 
                  "beans", "peas", "capsicum", "bell pepper", "garlic", "ginger", "gobi", "aloo",
                  "brinjal", "eggplant", "bhindi", "okra", "palak", "green chili", "curry leaves"],
    "grain": ["rice", "wheat", "flour", "atta", "maida", "suji", "semolina", "oats"],
    "protein": ["paneer", "chicken", "mutton", "egg", "dal", "lentil", "beans", "chickpeas", "chole", 
                "rajma", "kidney beans", "black gram", "urad dal"]
}

# Manual nutrition data for common ingredients that might be missing from DB
MANUAL_NUTRITION_DATA = {
    "chickpeas": {
        "calories": 364,
        "protein": 19.3,
        "carbs": 61.0,
        "fat": 6.0,
        "fiber": 17.0
    },
    "urad dal": {
        "calories": 341,
        "protein": 25.1,
        "carbs": 59.0,
        "fat": 1.6,
        "fiber": 18.3
    },
    "rajma": {
        "calories": 333,
        "protein": 24.0,
        "carbs": 60.0,
        "fat": 1.5,
        "fiber": 15.0
    },
    "whole wheat flour": {
        "calories": 340,
        "protein": 13.0,
        "carbs": 72.0,
        "fat": 1.7,
        "fiber": 11.2
    },
    "maida": {
        "calories": 348,
        "protein": 10.3,
        "carbs": 73.6,
        "fat": 1.2,
        "fiber": 2.7
    },
    "red chili powder": {
        "calories": 282,
        "protein": 12.0,
        "carbs": 56.6,
        "fat": 14.0,
        "fiber": 34.8
    },
    "coriander powder": {
        "calories": 279,
        "protein": 12.4,
        "carbs": 52.1,
        "fat": 16.1,
        "fiber": 41.9
    },
    "cumin powder": {
        "calories": 375,
        "protein": 18.0,
        "carbs": 44.2,
        "fat": 22.3,
        "fiber": 10.5
    },
    "oil": {
        "calories": 884,
        "protein": 0,
        "carbs": 0,
        "fat": 100,
        "fiber": 0
    },
    "vegetable oil": {
        "calories": 884,
        "protein": 0,
        "carbs": 0,
        "fat": 100,
        "fiber": 0
    },
    "potato": {
        "calories": 77,
        "protein": 2.0,
        "carbs": 17.0,
        "fat": 0.1,
        "fiber": 2.2
    },
    "green chili": {
        "calories": 40,
        "protein": 2.0,
        "carbs": 9.0,
        "fat": 0.2,
        "fiber": 1.5
    },
    "curry leaves": {
        "calories": 108,
        "protein": 6.0,
        "carbs": 18.7,
        "fat": 1.0,
        "fiber": 6.4
    },
    "dosa": {  # Per plain dosa without filling
        "calories": 120,
        "protein": 3.0, 
        "carbs": 20.0,
        "fat": 3.5,
        "fiber": 1.0
    },
    "masala dosa": {  # Per dosa with potato filling
        "calories": 180,
        "protein": 5.0,
        "carbs": 30.0,
        "fat": 7.0,
        "fiber": 3.0
    }
}

# Ingredient name mapping for common Indian ingredients
INGREDIENT_NAME_MAPPING = {
    "chickpeas": ["chickpeas", "chole", "chana", "garbanzo beans"],
    "urad dal": ["black lentils", "black gram", "urad dal", "black dal", "maa ki dal"],
    "rajma": ["red kidney beans", "rajma", "kidney beans"],
    "onion": ["onion", "onions", "pyaaz"],
    "tomato": ["tomato", "tomatoes", "tamatar"],
    "whole wheat flour": ["wheat flour", "atta", "chapati flour"],
    "maida": ["all-purpose flour", "maida", "refined flour", "white flour"],
    "oil": ["oil", "vegetable oil", "cooking oil", "sunflower oil", "refined oil"],
    "potato": ["potato", "potatoes", "aloo", "aaloo"],
    "green chili": ["green chili", "green chilies", "hari mirch", "green chilli"],
    "curry leaves": ["curry leaves", "curry leaf", "kadi patta"],
}

# Special case corrections for commonly mismatched ingredients
INGREDIENT_CORRECTIONS = {
    "green chili": "Green chili (Capsicum annuum)",
    "potato": "Potato (Solanum tuberosum)",
    "curry leaves": "Curry leaves",
    "ginger": "Ginger, fresh (Zingiber officinale)",
    "dosa": "Rice and lentil crepe (Dosa)"
}

def standardize_ingredients(ingredients_list):
    """
    Convert ingredients to standardized household measurements
    
    Args:
        ingredients_list (list): List of ingredients from recipe
    
    Returns:
        list: Standardized ingredients with weights in grams
    """
    standardized = []
    
    for ingredient in ingredients_list:
        try:
            name = ingredient.get("name", "").strip().lower()
            quantity = ingredient.get("quantity", "").strip().lower()
            
            # Fix common quantity errors
            quantity = fix_common_quantity_errors(name, quantity)
            
            # Skip ingredients that are marked as "to taste" or "for garnish"
            if "to taste" in quantity or "for garnish" in quantity or "as needed" in quantity:
                standardized.append({
                    "name": name,
                    "quantity": quantity,
                    "weight_grams": 0  # Zero weight for excluded ingredients
                })
                continue
                
            if not name or not quantity:
                continue
                
            # Extract numeric value and unit
            numeric_value, unit, size_desc = extract_quantity_and_unit(quantity, name)
            
            if numeric_value is None or unit is None:
                # If we can't parse, make an educated guess
                weight_grams = estimate_weight_from_description(name, quantity)
                standardized.append({
                    "name": normalize_ingredient_name(name),
                    "quantity": quantity,
                    "weight_grams": weight_grams
                })
                continue
                
            # Convert to standard unit and weight in grams
            weight_grams = convert_to_grams(numeric_value, unit, name, size_desc)
            
            standardized.append({
                "name": normalize_ingredient_name(name),
                "quantity": f"{numeric_value} {unit}",
                "weight_grams": weight_grams
            })
                
        except Exception as e:
            logger.warning(f"Error standardizing ingredient {ingredient}: {str(e)}")
            # Add with default values
            standardized.append({
                "name": normalize_ingredient_name(ingredient.get("name", "unknown")),
                "quantity": ingredient.get("quantity", "unknown"),
                "weight_grams": 50  # Default fallback weight
            })
    
    return standardized

def fix_common_quantity_errors(name, quantity):
    """Fix common errors in quantity measurements"""
    # Convert "for cooking" to estimated quantities
    if quantity == "for cooking" or quantity == "as needed for cooking":
        if "oil" in name or "ghee" in name:
            return "2 tablespoons"  # Standard amount for cooking
        
    # Fix curry leaves measured in liters
    if "curry" in name and "leaves" in name and "liter" in quantity:
        # Extract the number
        match = re.search(r'(\d+)', quantity)
        if match:
            number = match.group(1)
            return f"{number} leaves"
            
    return quantity

def normalize_ingredient_name(name):
    """Normalize ingredient names to standard forms"""
    name = name.lower().strip()
    
    # Replace commas and other modifiers
    name = re.sub(r',.*$', '', name)
    name = re.sub(r'\(.*?\)', '', name).strip()
    
    # Check against our mapping of common ingredients
    for standard_name, variations in INGREDIENT_NAME_MAPPING.items():
        if any(variation in name for variation in variations):
            return standard_name
            
    return name

def extract_quantity_and_unit(quantity_str, ingredient_name=None):
    """Extract numeric value, unit, and size description from quantity string"""
    # Default size
    size_desc = "default"
    
    # Handle fractions like 1/2
    quantity_str = quantity_str.replace("½", "0.5").replace("¼", "0.25").replace("¾", "0.75")
    
    # Check for size descriptions
    if "large" in quantity_str.lower():
        size_desc = "large"
    elif "medium" in quantity_str.lower():
        size_desc = "medium"
    elif "small" in quantity_str.lower():
        size_desc = "small"
    
    # Extract numeric value
    numeric_pattern = r'(\d+(?:\.\d+)?(?:/\d+)?)'
    numeric_match = re.search(numeric_pattern, quantity_str)
    
    if not numeric_match:
        return None, None, size_desc
    
    numeric_value = numeric_match.group(1)
    
    # Convert fraction to decimal
    if '/' in numeric_value:
        num, denom = numeric_value.split('/')
        numeric_value = float(num) / float(denom)
    else:
        numeric_value = float(numeric_value)
    
    # Extract unit
    unit_pattern = r'(?:' + '|'.join([
        'cup', 'tablespoon', 'tbsp', 'teaspoon', 'tsp', 'gram', 'g', 
        'kilogram', 'kg', 'ml', 'liter', 'l', 'piece', 'katori', 'glass',
        'leaves', 'leaf', 'inch'
    ]) + r')'
    
    unit_match = re.search(unit_pattern, quantity_str, re.IGNORECASE)
    
    if not unit_match:
        # If no standard unit, check for common words
        if 'pinch' in quantity_str:
            return numeric_value, "pinch", size_desc
        
        # Handle special case for curry leaves
        if "curry" in ingredient_name and "leaves" in quantity_str:
            return numeric_value, "leaves", size_desc
            
        # For common ingredients, apply default units
        if ingredient_name:
            if any(veg in ingredient_name for veg in ["onion", "tomato", "potato"]):
                return numeric_value, "piece", size_desc
        
        return numeric_value, "piece", size_desc
    
    unit = unit_match.group(0).lower()
    
    # Standardize units
    if unit in ['tbsp', 'tablespoon', 'tablespoons']:
        unit = 'tablespoon'
    elif unit in ['tsp', 'teaspoon', 'teaspoons']:
        unit = 'teaspoon'
    elif unit in ['g', 'gram', 'grams']:
        unit = 'gram'
    elif unit in ['kg', 'kilogram', 'kilograms']:
        unit = 'kilogram'
    elif unit in ['l', 'liter', 'liters']:
        unit = 'liter'
    elif unit in ['ml', 'milliliter', 'milliliters']:
        unit = 'ml'
    elif unit in ['leaf']:
        unit = 'leaf'
    elif unit in ['leaves']:
        unit = 'leaves'
    
    return numeric_value, unit, size_desc

def convert_to_grams(value, unit, ingredient_name, size_desc="default"):
    """Convert a measurement to grams based on the ingredient and unit"""
    ingredient_name = ingredient_name.lower()
    
    # Direct gram conversions
    if unit == 'gram':
        return value
    elif unit == 'kilogram':
        return value * 1000
    
    # Volume to weight conversions need ingredient category
    ingredient_category = determine_ingredient_category(ingredient_name)
    
    # Look up the conversion factor from household measures
    if unit in HOUSEHOLD_MEASURES:
        measure_dict = HOUSEHOLD_MEASURES[unit]
        
        # Handle special cases for specific ingredients
        if unit in ['leaf', 'leaves'] and 'curry' in ingredient_name:
            conversion_factor = measure_dict.get('curry leaf', measure_dict["default"])
            # For leaves, multiply by the number of leaves
            return value * conversion_factor
            
        # Special handling for pieces of vegetables
        if unit == 'piece' and ingredient_name in ['onion', 'tomato', 'potato'] and isinstance(measure_dict.get(ingredient_name), dict):
            return value * measure_dict[ingredient_name].get(size_desc, measure_dict[ingredient_name]["default"])
        
        # Check for exact ingredient match
        if ingredient_name in measure_dict:
            if isinstance(measure_dict[ingredient_name], dict):
                conversion_factor = measure_dict[ingredient_name].get(size_desc, measure_dict[ingredient_name]["default"])
            else:
                conversion_factor = measure_dict[ingredient_name]
        # Check for category match
        elif ingredient_category in measure_dict:
            conversion_factor = measure_dict[ingredient_category]
        # Use default
        else:
            conversion_factor = measure_dict["default"]
            
        return value * conversion_factor
    
    # Handle milliliters (assume 1ml = 1g for simplicity)
    elif unit == 'ml':
        return value
    elif unit == 'liter':
        return value * 1000
    
    # Handle special cases
    elif unit == 'pinch':
        return value * 0.5  # Assume a pinch is about 0.5g
    
    # Default case
    return value * 50  # Default fallback conversion

def determine_ingredient_category(ingredient_name):
    """Determine category of ingredient for conversion purposes"""
    ingredient_name = ingredient_name.lower()
    
    for category, items in INGREDIENT_CATEGORIES.items():
        for item in items:
            if item in ingredient_name:
                return category
    
    return "default"

def estimate_weight_from_description(name, quantity_str):
    """Make an educated guess about weight when parsing fails"""
    quantity_str = quantity_str.lower()
    name = name.lower()
    
    # First check if it's "for cooking"
    if "for cooking" in quantity_str:
        if "oil" in name or "ghee" in name:
            return 30  # About 2 tablespoons
        if "salt" in name:
            return 5   # About 1 teaspoon
    
    # Check for common descriptors
    if "handful" in quantity_str:
        return 30
    elif "pinch" in quantity_str:
        return 1
    elif any(word in quantity_str for word in ["small", "little"]):
        return 25
    elif any(word in quantity_str for word in ["large", "big"]):
        return 100
    elif "medium" in quantity_str:
        return 60
    
    # Guess based on ingredient type
    for category, items in INGREDIENT_CATEGORIES.items():
        for item in items:
            if item in name:
                if category == "spice":
                    return 5
                elif category == "vegetable":
                    return 80
                elif category == "liquid":
                    return 100
                elif category == "grain":
                    return 100
                elif category == "protein":
                    if "chickpeas" in name or "chole" in name:
                        return 150
                    return 150
    
    # Default fallback
    return 50

def map_ingredients_to_nutrition(standardized_ingredients, db):
    """
    Map ingredients to nutrition database and calculate total nutrition
    
    Args:
        standardized_ingredients (list): Standardized ingredients with weights
        db: Database connection object
    
    Returns:
        tuple: (total nutrition dict, list of ingredients with mapped nutrition)
    """
    total_nutrition = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0
    }
    
    ingredients_with_nutrition = []
    
    for ingredient in standardized_ingredients:
        try:
            name = ingredient["name"]
            weight_grams = ingredient["weight_grams"]
            
            # Skip ingredients with zero weight (usually "to taste" or garnish)
            if weight_grams <= 0:
                ingredients_with_nutrition.append({
                    "ingredient": name,
                    "quantity": ingredient["quantity"],
                    "matched_to": "Excluded from calculation"
                })
                continue
            
            # Check for special case corrections first
            if name in INGREDIENT_CORRECTIONS:
                matched_name = INGREDIENT_CORRECTIONS[name]
                
                # First check if we have manual nutrition data
                manual_match = get_manual_nutrition_data(name)
                if manual_match:
                    nutrition = calculate_manual_ingredient_nutrition(manual_match, weight_grams)
                    for key in total_nutrition:
                        if key in nutrition:
                            total_nutrition[key] += nutrition[key]
                    
                    ingredients_with_nutrition.append({
                        "ingredient": name,
                        "quantity": ingredient["quantity"],
                        "matched_to": matched_name
                    })
                    continue
                else:
                    # Try to find corrected name in database
                    db_ingredient = find_ingredient_in_db(db, matched_name)
                    if db_ingredient:
                        nutrition = calculate_ingredient_nutrition(db_ingredient, weight_grams)
                        for key in total_nutrition:
                            if key in nutrition:
                                total_nutrition[key] += nutrition[key]
                        
                        ingredients_with_nutrition.append({
                            "ingredient": name,
                            "quantity": ingredient["quantity"],
                            "matched_to": matched_name
                        })
                        continue
            
            # First check if we have manual nutrition data
            manual_match = get_manual_nutrition_data(name)
            if manual_match:
                nutrition = calculate_manual_ingredient_nutrition(manual_match, weight_grams)
                for key in total_nutrition:
                    if key in nutrition:
                        total_nutrition[key] += nutrition[key]
                
                ingredients_with_nutrition.append({
                    "ingredient": name,
                    "quantity": ingredient["quantity"],
                    "matched_to": f"{name} (standard values)"
                })
                continue
            
            # Find ingredient in database
            db_ingredient = find_ingredient_in_db(db, name)
            
            if not db_ingredient:
                # If not found, try fuzzy matching
                db_ingredient = fuzzy_match_ingredient(db, name)
            
            if db_ingredient:
                # Calculate nutrition based on weight
                nutrition = calculate_ingredient_nutrition(db_ingredient, weight_grams)
                
                # Add to total
                for key in total_nutrition:
                    if key in nutrition:
                        total_nutrition[key] += nutrition[key]
                
                matched_name = db_ingredient.get("name", db_ingredient.get("food_name", "unknown"))
                ingredients_with_nutrition.append({
                    "ingredient": name,
                    "quantity": ingredient["quantity"],
                    "matched_to": matched_name
                })
            else:
                # Ingredient not found, but still add a reasonable estimate based on category
                estimated_nutrition = estimate_nutrition_by_category(name, weight_grams)
                
                # Add estimated nutrition to total
                for key in total_nutrition:
                    if key in estimated_nutrition:
                        total_nutrition[key] += estimated_nutrition[key]
                
                ingredients_with_nutrition.append({
                    "ingredient": name,
                    "quantity": ingredient["quantity"],
                    "matched_to": "estimated values"
                })
        except Exception as e:
            logger.error(f"Error processing ingredient {ingredient.get('name', 'unknown')}: {str(e)}")
            # In case of error, still add the ingredient to the list without affecting nutrition totals
            ingredients_with_nutrition.append({
                "ingredient": ingredient.get("name", "unknown"),
                "quantity": ingredient.get("quantity", "unknown"),
                "matched_to": "not calculated (error)"
            })
    
    # Apply some validation and sanity checks to the nutrition totals
    validate_nutrition_totals(total_nutrition, ingredients_with_nutrition)
    
    return total_nutrition, ingredients_with_nutrition

def get_manual_nutrition_data(ingredient_name):
    """Check if we have manual nutrition data for this ingredient"""
    for name, data in MANUAL_NUTRITION_DATA.items():
        if name in ingredient_name:
            return data
    return None

def calculate_manual_ingredient_nutrition(nutrition_data, weight_grams):
    """Calculate nutrition for a specific ingredient based on weight using manual data"""
    nutrition = {}
    
    # Nutrition values are per 100g
    ratio = weight_grams / 100.0
    
    for key, value in nutrition_data.items():
        nutrition[key] = value * ratio
    
    return nutrition

def estimate_nutrition_by_category(ingredient_name, weight_grams):
    """Provide a reasonable nutrition estimate based on ingredient category"""
    category = determine_ingredient_category(ingredient_name)
    
    # Default nutrition values per 100g for different categories
    category_nutrition = {
        "spice": {
            "calories": 250,
            "protein": 10,
            "carbs": 50,
            "fat": 10,
            "fiber": 30
        },
        "vegetable": {
            "calories": 65,
            "protein": 3,
            "carbs": 12,
            "fat": 0.5,
            "fiber": 4
        },
        "grain": {
            "calories": 350,
            "protein": 10,
            "carbs": 70,
            "fat": 2,
            "fiber": 10
        },
        "protein": {
            "calories": 300,
            "protein": 20,
            "carbs": 40,
            "fat": 5,
            "fiber": 10
        },
        "liquid": {
            "calories": 40,
            "protein": 1,
            "carbs": 5,
            "fat": 1,
            "fiber": 0
        },
        "default": {
            "calories": 150,
            "protein": 5,
            "carbs": 20,
            "fat": 5,
            "fiber": 5
        }
    }
    
    # Get nutrition values for this category
    nutrition_values = category_nutrition.get(category, category_nutrition["default"])
    
    # Calculate nutrition based on weight
    ratio = weight_grams / 100.0
    nutrition = {}
    
    for key, value in nutrition_values.items():
        nutrition[key] = value * ratio
    
    return nutrition

def fuzzy_match_ingredient(db, ingredient_name):
    """Use fuzzy matching to find the closest ingredient in database"""
    try:
        collection = db["nutrition_source"]
        
        # Get all ingredient names from database
        all_ingredients = []
        cursor = collection.find({}, {"food_name": 1})
        for doc in cursor:
            if "food_name" in doc:
                all_ingredients.append(doc["food_name"])
        
        if not all_ingredients:
            return None
            
        # Find closest match
        best_match, score = process.extractOne(ingredient_name, all_ingredients)
        
        # Only accept match if score is above threshold
        if score >= 70:
            result = collection.find_one({"food_name": best_match})
            logger.info(f"Fuzzy matched {ingredient_name} to {best_match} with score {score}")
            return result
    
    except Exception as e:
        logger.error(f"Error in fuzzy matching: {str(e)}")
    
    return None

def calculate_ingredient_nutrition(db_ingredient, weight_grams):
    """Calculate nutrition for a specific ingredient based on weight"""
    nutrition = {}
    
    # Nutrition values in database are per 100g
    ratio = weight_grams / 100.0
    
    # Map to the correct field names based on the database structure
    nutrition_mapping = {
        "calories": "energy_kcal",
        "protein": "protein_g",
        "carbs": "carb_g",
        "fat": "fat_g",
        "fiber": "fibre_g"
    }
    
    for key, db_key in nutrition_mapping.items():
        if db_key in db_ingredient and db_ingredient[db_key] is not None:
            nutrition[key] = db_ingredient[db_key] * ratio
    
    return nutrition

def validate_nutrition_totals(nutrition_totals, ingredients):
    """Apply validation and sanity checks to calculated nutrition totals"""
    # Check if calories seem reasonable (not too low)
    if nutrition_totals["calories"] < 50 and len(ingredients) > 3:
        # This is likely too low, apply a multiplier
        logger.warning("Calculated calories too low, applying correction factor")
        multiplier = 250 / max(nutrition_totals["calories"], 1)  # Ensure we don't divide by zero
        multiplier = min(multiplier, 10)  # Cap the multiplier at 10x
        
        for key in nutrition_totals:
            nutrition_totals[key] *= multiplier
    
    # Check if fiber content is unrealistically high (more than 30% of total weight)
    total_weight_estimate = (nutrition_totals["protein"] + 
                             nutrition_totals["carbs"] + 
                             nutrition_totals["fat"] +
                             nutrition_totals["fiber"])
    
    if nutrition_totals["fiber"] > 0.3 * total_weight_estimate:
        logger.warning("Fiber content unrealistically high, adjusting down")
        nutrition_totals["fiber"] = 0.15 * total_weight_estimate  # Set to a more reasonable 15%
    
    # Cap fiber at realistic levels for Indian dishes
    if nutrition_totals["fiber"] > 10:
        logger.warning(f"Capping unrealistically high fiber: {nutrition_totals['fiber']:.1f}g → 8.0g")
        nutrition_totals["fiber"] = 8.0
    
    # Check if macros add up (protein + carbs + fat should be reasonable compared to calories)
    calorie_from_macros = (nutrition_totals["protein"] * 4 + 
                           nutrition_totals["carbs"] * 4 + 
                           nutrition_totals["fat"] * 9)
    
    # If there's a huge discrepancy, adjust
    if calorie_from_macros > 0 and abs(nutrition_totals["calories"] - calorie_from_macros) / calorie_from_macros > 0.5:
        logger.warning("Calories don't match macros, adjusting")
        nutrition_totals["calories"] = calorie_from_macros
    
    # Ensure minimum reasonable values for a dish
    min_values = {
        "calories": 100,
        "protein": 2,
        "carbs": 10,
        "fat": 2,
        "fiber": 1
    }
    
    for key, min_val in min_values.items():
        if nutrition_totals[key] < min_val:
            nutrition_totals[key] = min_val
