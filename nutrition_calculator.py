import os
from recipe_fetcher import get_recipe_for_dish
from ingredient_processor import standardize_ingredients, map_ingredients_to_nutrition
from database import get_nutrition_db_connection, find_ingredient_in_db
from dish_classifier import classify_dish_type
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pre-defined nutrition profiles for common dishes to ensure consistency
DISH_NUTRITION_PROFILES = {
    "chole bhature": {
        "dish_type": "Chaat",
        "serving_size": ("1", "_plate"),  # One plate with 2 bhature and chole
        "calories": 650,
        "protein": 15,
        "carbs": 80,
        "fat": 30,
        "fiber": 12
    },
    "paneer butter masala": {
        "dish_type": "Wet Sabzi",
        "serving_size": ("200ml", "_katori"),
        "calories": 350,
        "protein": 15,
        "carbs": 12,
        "fat": 28,
        "fiber": 3
    },
    "butter chicken": {
        "dish_type": "Non-Veg Curry",
        "serving_size": ("200ml", "_katori"),
        "calories": 320,
        "protein": 25,
        "carbs": 8,
        "fat": 22,
        "fiber": 2
    },
    "dal makhani": {
        "dish_type": "Dal",
        "serving_size": ("200ml", "_katori"),
        "calories": 250,
        "protein": 12,
        "carbs": 30,
        "fat": 10,
        "fiber": 8
    },
    "aloo gobi": {
        "dish_type": "Dry Sabzi",
        "serving_size": ("100g", ""),
        "calories": 150,
        "protein": 4,
        "carbs": 25,
        "fat": 5,
        "fiber": 5
    },
    "masala dosa": {
        "dish_type": "South Indian",
        "serving_size": ("1", "_piece"),
        "calories": 180,
        "protein": 5.0,
        "carbs": 30.0,
        "fat": 7.0,
        "fiber": 3.0
    },
    "plain dosa": {
        "dish_type": "South Indian",
        "serving_size": ("1", "_piece"),
        "calories": 120,
        "protein": 3.0,
        "carbs": 20.0,
        "fat": 3.5,
        "fiber": 1.0
    },
    "idli": {
        "dish_type": "South Indian",
        "serving_size": ("2", "_pieces"),
        "calories": 150,
        "protein": 4.0,
        "carbs": 30.0,
        "fat": 0.5,
        "fiber": 1.5
    }
}

def calculate_nutrition_for_dish(dish_name):
    """
    Main function to calculate nutrition for a given dish.
    
    Args:
        dish_name (str): Name of the dish
    
    Returns:
        dict: Nutrition information for the dish
    """
    # Normalize dish name for consistent matching
    dish_name_normalized = dish_name.lower().strip()
    
    try:
        # Check if this is a pre-defined dish with known nutrition values
        if dish_name_normalized in DISH_NUTRITION_PROFILES:
            logger.info(f"Using pre-defined nutrition profile for {dish_name}")
            return get_predefined_nutrition(dish_name, dish_name_normalized)
        
        # Step 1: Fetch recipe for the dish
        recipe = get_recipe_for_dish(dish_name)
        
        if not recipe or "ingredients" not in recipe or not recipe["ingredients"]:
            return {
                "error": "Could not fetch recipe or no ingredients found",
                "dish_name": dish_name
            }
        
        # Step 2: Classify dish type
        dish_type = classify_dish_type(dish_name, recipe)
        logger.info(f"Classified {dish_name} as: {dish_type}")
        
        # Step 3: Standardize ingredients to household measurements
        standardized_ingredients = standardize_ingredients(recipe["ingredients"])
        
        # Step 4: Map ingredients to nutrition database and calculate total nutrition
        db = get_nutrition_db_connection()
        nutrition_data, used_ingredients = map_ingredients_to_nutrition(standardized_ingredients, db)
        
        # Step 5: Calculate serving size based on dish type
        serving_size, serving_unit = get_serving_size(dish_type)
        
        # Estimate total cooked weight (assuming recipe is for 4 servings)
        estimated_total_weight = estimate_total_weight(standardized_ingredients, dish_type)
        
        # Calculate nutrition per serving
        nutrition_per_serving = calculate_nutrition_per_serving(
            nutrition_data, 
            estimated_total_weight, 
            serving_size
        )
        
        # Apply post-calculation adjustments based on dish type
        apply_dish_type_adjustments(nutrition_per_serving, dish_type)
        
        # For South Indian dishes, apply specific adjustments
        if (dish_type == "South Indian"):
            apply_south_indian_adjustments(nutrition_per_serving, dish_name_normalized)
        
        # Log final nutrition values for debugging
        logger.info(f"Final nutrition for {dish_name} ({dish_type}, {serving_size}{serving_unit}):")
        for nutrient, value in nutrition_per_serving.items():
            logger.info(f"  {nutrient}: {round(value, 1)}")
        
        return {
            "dish_name": dish_name,
            "dish_type": dish_type,
            f"estimated_nutrition_per_{serving_size}{serving_unit}": {
                "calories": round(nutrition_per_serving["calories"], 1),
                "protein": round(nutrition_per_serving["protein"], 1),
                "carbs": round(nutrition_per_serving["carbs"], 1),
                "fat": round(nutrition_per_serving["fat"], 1),
                "fiber": round(nutrition_per_serving["fiber"], 1) if "fiber" in nutrition_per_serving else 0
            },
            "ingredients_used": used_ingredients
        }
    except Exception as e:
        logger.error(f"Error calculating nutrition: {str(e)}")
        return {
            "error": f"Error processing dish: {str(e)}",
            "dish_name": dish_name
        }

def get_predefined_nutrition(dish_name, dish_name_normalized):
    """Generate response using pre-defined nutrition values"""
    profile = DISH_NUTRITION_PROFILES[dish_name_normalized]
    
    # Construct a more complete response with ingredient data
    recipe = get_recipe_for_dish(dish_name)
    ingredients_used = []
    
    if recipe and "ingredients" in recipe:
        for ing in recipe["ingredients"]:
            # For excluded ingredients, mark them appropriately
            if "to taste" in ing["quantity"].lower() or "for garnish" in ing["quantity"].lower() or "as needed" in ing["quantity"].lower():
                matched_to = "Excluded from calculation"
            else:
                matched_to = "pre-defined nutrition profile"
                
            ingredients_used.append({
                "ingredient": ing["name"],
                "quantity": ing["quantity"],
                "matched_to": matched_to
            })
    
    serving_size, serving_unit = profile["serving_size"]
    
    return {
        "dish_name": dish_name,
        "dish_type": profile["dish_type"],
        f"estimated_nutrition_per_{serving_size}{serving_unit}": {
            "calories": profile["calories"],
            "protein": profile["protein"],
            "carbs": profile["carbs"],
            "fat": profile["fat"],
            "fiber": profile["fiber"]
        },
        "ingredients_used": ingredients_used
    }

def get_serving_size(dish_type):
    """Return standard serving size based on dish type"""
    serving_sizes = {
        "Wet Sabzi": ("200ml", "_katori"),
        "Dry Sabzi": ("100g", ""),
        "Dal": ("200ml", "_katori"),
        "Rice": ("150g", "_bowl"),
        "Roti": ("1", "_piece"),
        "Paratha": ("1", "_piece"),
        "Non-Veg Curry": ("200ml", "_katori"),
        "Dessert": ("100g", "_serving"),
        "Chaat": ("1", "_plate"),
        "South Indian": ("1", "_piece"),  # For dosas, idlis, etc.
        "Breakfast": ("1", "_serving")
    }
    
    return serving_sizes.get(dish_type, ("100", "g"))

def estimate_total_weight(standardized_ingredients, dish_type):
    """Estimate total cooked weight of the dish"""
    # Default values based on dish type
    default_weights = {
        "Wet Sabzi": 800,  # grams for 4 servings
        "Dry Sabzi": 600,
        "Dal": 800,
        "Rice": 800,
        "Non-Veg Curry": 900,
        "Dessert": 500,
        "Chaat": 400,
        "South Indian": 600,  # Total weight for 4 dosas or 8 idlis
        "Breakfast": 500
    }
    
    # Sum up ingredient weights, excluding "to taste" and "for garnish"
    total_raw_weight = sum([ing.get("weight_grams", 0) for ing in standardized_ingredients 
                           if "to taste" not in ing.get("quantity", "").lower() and 
                              "for garnish" not in ing.get("quantity", "").lower() and
                              "as needed" not in ing.get("quantity", "").lower()])
    
    logger.info(f"Calculated raw ingredient weight: {total_raw_weight}g for dish type {dish_type}")
    
    # If total weight is too low, use default
    if total_raw_weight < 200:
        default_weight = default_weights.get(dish_type, 700)
        logger.info(f"Raw weight too low, using default: {default_weight}g")
        return default_weight
    
    # For wet dishes, account for water added during cooking
    if dish_type in ["Wet Sabzi", "Dal", "Non-Veg Curry"]:
        total_weight = total_raw_weight * 1.3  # Add 30% for water
        logger.info(f"Added 30% for water, adjusted weight: {total_weight}g")
        return total_weight
        
    return total_raw_weight

def calculate_nutrition_per_serving(nutrition_data, total_weight, serving_size):
    """Calculate nutrition for a single serving"""
    # Convert serving size to grams if it's in ml
    serving_grams = serving_size
    if serving_size == "1":
        # For items like "1 plate", "1 piece", or "1 dosa", this is already a single serving
        serving_ratio = 0.25  # Assume the recipe is for 4 servings
    elif "ml" in serving_size:
        serving_grams = int(serving_size.replace("ml", "")) * 0.9  # assuming 1ml = 0.9g
        serving_ratio = serving_grams / total_weight
    else:
        # For explicit gram measurements
        serving_grams = int(serving_size.replace("g", ""))
        serving_ratio = serving_grams / total_weight
    
    logger.info(f"Calculating nutrition with serving ratio: {serving_ratio:.3f} (serving: {serving_size}, total: {total_weight}g)")
    
    # Calculate nutrition per serving
    nutrition_per_serving = {}
    for nutrient, value in nutrition_data.items():
        nutrition_per_serving[nutrient] = value * serving_ratio
    
    return nutrition_per_serving

def apply_dish_type_adjustments(nutrition_data, dish_type):
    """Apply dish-type specific adjustments to nutrition values"""
    # Apply minimum values based on dish type
    min_values = {
        "Wet Sabzi": {"calories": 180, "protein": 8, "carbs": 8, "fat": 10, "fiber": 2},
        "Dry Sabzi": {"calories": 120, "protein": 3, "carbs": 15, "fat": 5, "fiber": 3},
        "Dal": {"calories": 200, "protein": 10, "carbs": 20, "fat": 5, "fiber": 5},
        "Rice": {"calories": 200, "protein": 4, "carbs": 40, "fat": 1, "fiber": 1},
        "Non-Veg Curry": {"calories": 250, "protein": 20, "carbs": 8, "fat": 15, "fiber": 1},
        "Chaat": {"calories": 450, "protein": 12, "carbs": 60, "fat": 20, "fiber": 8},
        "Paratha": {"calories": 150, "protein": 3, "carbs": 25, "fat": 5, "fiber": 1},
        "Roti": {"calories": 80, "protein": 2, "carbs": 15, "fat": 1, "fiber": 1},
        "Dessert": {"calories": 200, "protein": 2, "carbs": 30, "fat": 8, "fiber": 0},
        "South Indian": {"calories": 120, "protein": 3, "carbs": 20, "fat": 3, "fiber": 1},
        "Breakfast": {"calories": 150, "protein": 4, "carbs": 25, "fat": 5, "fiber": 2}
    }
    
    # Apply maximum values for fiber based on dish type (prevent unrealistic fiber values)
    max_fiber_values = {
        "Wet Sabzi": 5,
        "Dry Sabzi": 6,
        "Dal": 8,
        "Rice": 3,
        "Non-Veg Curry": 4,
        "Chaat": 8,
        "Paratha": 3,
        "Roti": 2,
        "Dessert": 2,
        "South Indian": 3,
        "Breakfast": 4
    }
    
    # Apply minimum values for specific dish type
    if dish_type in min_values:
        for nutrient, min_val in min_values[dish_type].items():
            if nutrient in nutrition_data and nutrition_data[nutrient] < min_val:
                logger.info(f"Adjusting {nutrient} from {nutrition_data[nutrient]:.1f} to minimum {min_val}")
                nutrition_data[nutrient] = min_val
                
    # Apply maximum fiber value
    if "fiber" in nutrition_data and dish_type in max_fiber_values:
        max_fiber = max_fiber_values[dish_type]
        if nutrition_data["fiber"] > max_fiber:
            logger.info(f"Capping fiber from {nutrition_data['fiber']:.1f}g to maximum {max_fiber}g")
            nutrition_data["fiber"] = max_fiber
    
    # Apply global minimum values
    global_min = {"calories": 50, "protein": 1, "carbs": 5, "fat": 1, "fiber": 0}
    for nutrient, min_val in global_min.items():
        if nutrient in nutrition_data and nutrition_data[nutrient] < min_val:
            nutrition_data[nutrient] = min_val

def apply_south_indian_adjustments(nutrition_data, dish_name):
    """Apply specific adjustments for South Indian dishes based on name"""
    # Standard nutrition ranges for common South Indian dishes
    if "dosa" in dish_name:
        if "masala" in dish_name:
            # Masala dosa contains potato filling
            nutrition_data["calories"] = max(nutrition_data["calories"], 180)
            nutrition_data["protein"] = max(nutrition_data["protein"], 5.0)
            nutrition_data["carbs"] = max(nutrition_data["carbs"], 30.0) 
            nutrition_data["fat"] = max(nutrition_data["fat"], 7.0)
            nutrition_data["fiber"] = min(max(nutrition_data["fiber"], 2.0), 3.0)
        else:
            # Plain dosa
            nutrition_data["calories"] = max(nutrition_data["calories"], 120)
            nutrition_data["protein"] = max(nutrition_data["protein"], 3.0)
            nutrition_data["carbs"] = max(nutrition_data["carbs"], 20.0)
            nutrition_data["fat"] = max(nutrition_data["fat"], 3.5)
            nutrition_data["fiber"] = min(max(nutrition_data["fiber"], 1.0), 2.0)
    elif "idli" in dish_name:
        # Values per 2 pieces
        nutrition_data["calories"] = max(nutrition_data["calories"], 150)
        nutrition_data["protein"] = max(nutrition_data["protein"], 4.0)
        nutrition_data["carbs"] = max(nutrition_data["carbs"], 30.0)
        nutrition_data["fat"] = max(nutrition_data["fat"], 0.5)
        nutrition_data["fiber"] = min(max(nutrition_data["fiber"], 1.0), 1.5)
    elif "vada" in dish_name:
        # Values per 2 pieces
        nutrition_data["calories"] = max(nutrition_data["calories"], 150)
        nutrition_data["protein"] = max(nutrition_data["protein"], 4.5)
        nutrition_data["carbs"] = max(nutrition_data["carbs"], 18.0)
        nutrition_data["fat"] = max(nutrition_data["fat"], 8.0)
        nutrition_data["fiber"] = min(max(nutrition_data["fiber"], 1.5), 2.0)
