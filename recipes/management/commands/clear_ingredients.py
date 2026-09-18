from django.core.management.base import BaseCommand
from recipes.models import Ingredient, IngredientNutrientRelationship
class Command(BaseCommand):
    help = 'Clear ingredient nutrient data'

    def handle(self, *args, **kwargs):
        
        rel_count = IngredientNutrientRelationship.objects.count()
        IngredientNutrientRelationship.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'✓ Cleared {rel_count} nutrient relationships')
        )

        ing_count = Ingredient.objects.count()
        Ingredient.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'✓ Cleared {ing_count} ingredients')
        )