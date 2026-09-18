import json
from django.core.management.base import BaseCommand
from ._utils import get_ingredients_path, get_ingredients_nutrition_path

class Command(BaseCommand):
    help = "Extract ingredient data from previous search"

    def handle(self, *args, **kwargs):
        # Load existing ingredient_nutrients.json
        with open(get_ingredients_nutrition_path()) as f:
            ingredient_nutrients = json.load(f)

        # Extract unique ingredients with their fdcIds
        ingredients = [
            {
                "name": row["ingredient"],
                "fdcId": str(row["fdcId"])
            }
            for row in ingredient_nutrients
        ]

        # Write new ingredients.json
        with open(get_ingredients_path(), 'w') as f:
            json.dump(ingredients, f, indent=4)

        print(f'✓ Extracted {len(ingredients)} ingredients')