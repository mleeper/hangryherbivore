# recipes/management/commands/load_nutrients.py
from pathlib import Path
import json
from django.core.management.base import BaseCommand
from recipes.models import Nutrient
from ._utils import get_nutrients_path

class Command(BaseCommand):
    help = 'Load initial nutrients'

    def handle(self, *args, **kwargs):
        
        with open(get_nutrients_path()) as f:
            nutrients = json.load(f)

        for nutrient in nutrients:
            Nutrient.objects.get_or_create(
                name=nutrient['name'],
                defaults={'unit': nutrient['unit']}
            )
            self.stdout.write(f"✓ {nutrient['name']}")

        self.stdout.write(self.style.SUCCESS('Nutrients loaded!'))
        