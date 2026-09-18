import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path
import json
from django.core.management.base import BaseCommand
from recipes.models import Nutrient
from ._utils import fetch_ingredient_nutrients, get_ingredients_path, get_nutrients_path, get_ingredients_nutrition_path

class Command(BaseCommand):
    help = "Import ingredients"
    
    def handle(self, *args, **kwargs):
        load_dotenv()
        API_KEY = os.getenv("USDA_KEY")

        ingredients_nutrition = []

        with open(get_nutrients_path()) as f:
            nutrients = json.load(f)
        
        target_nutrients = {item["usdaid"]: item["name"] for item in nutrients if "usdaid" in item and "name" in item}

        with open(get_ingredients_path()) as f:
            ingredients = json.load(f)

        for ingredient in ingredients:
            print(f"Processing: {ingredient["name"]}...")
            ingredient_profile = fetch_ingredient_nutrients(API_KEY, ingredient["fdcId"], ingredient["name"], target_nutrients)

            if ingredient_profile:
                ingredients_nutrition.append(ingredient_profile)

            # Respect API rate limits (standard key permits 1,000 requests per hour)
            time.sleep(1)

        # Save data locally to a clean JSON file
        with open(get_ingredients_nutrition_path(), "w", encoding="utf-8") as f:
            json.dump(ingredients_nutrition, f, indent=4)

        print("\n✅ Extraction complete! File saved as ingredients_nutrition.json")