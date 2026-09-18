import requests
from pathlib import Path

LIQUID_KEYWORDS = [
    # Obvious liquids
    'liquid', 'juice', 'water', 'wine', 'beer',
    'broth', 'stock', 'spirits',
    
    # Dairy and alternatives
    'milk', 'cream', 'yogurt',
    
    # Oils and fats
    'oil',
    
    # Vinegars and acids
    'vinegar',
    
    # Sauces and condiments
    'sauce', 'ketchup', 'tamari',
    
    # Sweeteners
    'syrup', 'molasses', 'nectar',
    
    # Beverages
    'tea', 'chai', 'coffee',
    
    # Extracts
    'extract',
]

LIQUID_EXCLUSIONS = [
    'powder',
    'leaf',
    'leaves',
    'dried',
    'ground',
    'seeds',
    'flakes',
]

def get_ingredients_path():
    return Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'ingredients.json'

def get_nutrients_path():
    return Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'nutrients.json'

def get_ingredients_nutrition_path():
    return Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'ingredients_nutrition.json'

def fetch_ingredient_nutrients(api_key, fdcId, ingredient_name, target_nutrients):
    endpoint = f"https://api.nal.usda.gov/fdc/v1/food/{fdcId}"
    params = {"api_key": api_key}

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"❌ No matches found for: {ingredient_name}")
            return None

        extracted_nutrients = {
            "ingredient": ingredient_name,
            "fdcId": data.get("fdcId"),
            "description": data.get("description"),
            "nutrients": {},
        }

        # Filter out only your allowed list of nutrients
        for food_nutrient in data.get("foodNutrients", []):
            # USDA returns nutrientId as an int or string depending on schema version
            nutrient = food_nutrient.get("nutrient", {})
            n_id = str(nutrient.get("number", ''))
            if n_id in target_nutrients:
                label = target_nutrients[n_id]
                extracted_nutrients["nutrients"][label] = food_nutrient.get("amount", 0)
        return extracted_nutrients

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching {ingredient_name}: {e}")
        return None

def is_liquid(name):
    name_lower = name.lower()
    for exclusion in LIQUID_EXCLUSIONS:
        if exclusion.lower() in name_lower:
            return False

    return any(keyword in name_lower for keyword in LIQUID_KEYWORDS)