# recipes/management/commands/load_nutrients.py
from pathlib import Path
import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, IngredientNutrientRelationship, Nutrient
from ._utils import get_ingredients_nutrition_path, is_liquid

class Command(BaseCommand):
    help = 'Load initial ingredients'

    def handle(self, *args, **kwargs):
        
        with open(get_ingredients_nutrition_path()) as f:
            ingredients = json.load(f)

        for row in ingredients:
            ingredient_name = row['ingredient']
            is_liquid_ingredient = is_liquid(ingredient_name)
            # Step 1 - Get or create ingredient
            ingredient, created = Ingredient.objects.get_or_create(
                name=ingredient_name,
                defaults={
                    'is_liquid': is_liquid_ingredient,
                    'fdcId': row.get('fdcId'),
                }
            )

            action = 'Created' if created else 'Exists'
            self.stdout.write(f'✓ {action}: {ingredient_name}')

            # Step 2 - Attach nutrients
            nutrients = row.get('nutrients', {})

            if not nutrients:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠ No nutrients for {ingredient_name}')
                )
                continue
            
            for nutrient_name, amount in nutrients.items():
                nutrient = Nutrient.objects.filter(name=nutrient_name).first()

                if not nutrient:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Nutrient not found: {nutrient_name} — skipping')
                    )
                    continue

                IngredientNutrientRelationship.objects.update_or_create(
                    ingredient=ingredient,
                    nutrient=nutrient,
                    defaults={'amount': round(amount, 2)}
                )

            self.stdout.write(
                f'  ✓ {len(nutrients)} nutrients attached'
            )

        self.stdout.write(self.style.SUCCESS('\n✓ All ingredients loaded!'))
        