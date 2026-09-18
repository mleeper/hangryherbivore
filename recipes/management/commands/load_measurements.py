# management/commands/load_measurements.py
from django.core.management.base import BaseCommand
from recipes.models import MeasurementConversion

class Command(BaseCommand):
    help = 'Load common measurement conversions'

    MEASUREMENTS = [
        # Flours & Powders
        {'ingredient_name': 'All Purpose Flour',   'category': 'flour_powder', 'us_quantity': 1,   'us_unit': 'cup', 'metric_quantity': 120, 'metric_unit': 'g'},
        {'ingredient_name': 'Whole Wheat Flour',   'category': 'flour_powder', 'us_quantity': 1,   'us_unit': 'cup', 'metric_quantity': 130, 'metric_unit': 'g'},
        {'ingredient_name': 'Almond Flour',        'category': 'flour_powder', 'us_quantity': 1,   'us_unit': 'cup', 'metric_quantity': 96,  'metric_unit': 'g'},
        {'ingredient_name': 'Chickpea Flour',      'category': 'flour_powder', 'us_quantity': 1,   'us_unit': 'cup', 'metric_quantity': 92,  'metric_unit': 'g'},
        {'ingredient_name': 'Baking Powder',       'category': 'flour_powder', 'us_quantity': 1,   'us_unit': 'tsp', 'metric_quantity': 4,   'metric_unit': 'g'},
        {'ingredient_name': 'Baking Soda',         'category': 'flour_powder', 'us_quantity': 1,   'us_unit': 'tsp', 'metric_quantity': 6,   'metric_unit': 'g'},

        # Grains & Legumes
        {'ingredient_name': 'Rolled Oats',         'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 90,  'metric_unit': 'g'},
        {'ingredient_name': 'Steel Cut Oats',      'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 160, 'metric_unit': 'g'},
        {'ingredient_name': 'White Rice',          'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 185, 'metric_unit': 'g'},
        {'ingredient_name': 'Green Lentils',       'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 200, 'metric_unit': 'g'},
        {'ingredient_name': 'Red Lentils',         'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 190, 'metric_unit': 'g'},
        {'ingredient_name': 'Black Beans (dry)',   'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 180, 'metric_unit': 'g'},
        {'ingredient_name': 'Chickpeas (dry)',     'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 200, 'metric_unit': 'g'},
        {'ingredient_name': 'Pearl Barley',        'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 200, 'metric_unit': 'g'},
        {'ingredient_name': 'Quinoa',              'category': 'grains_legumes', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 170, 'metric_unit': 'g'},

        # Liquids
        {'ingredient_name': 'Water',               'category': 'liquids', 'us_quantity': 1,    'us_unit': 'cup',  'metric_quantity': 240, 'metric_unit': 'ml'},
        {'ingredient_name': 'Coconut Milk',        'category': 'liquids', 'us_quantity': 1,    'us_unit': 'cup',  'metric_quantity': 240, 'metric_unit': 'ml'},
        {'ingredient_name': 'Coconut Cream',       'category': 'liquids', 'us_quantity': 1,    'us_unit': 'cup',  'metric_quantity': 240, 'metric_unit': 'ml'},
        {'ingredient_name': 'Soy Milk',            'category': 'liquids', 'us_quantity': 1,    'us_unit': 'cup',  'metric_quantity': 240, 'metric_unit': 'ml'},
        {'ingredient_name': 'Olive Oil',           'category': 'liquids', 'us_quantity': 1,    'us_unit': 'tbsp', 'metric_quantity': 14,  'metric_unit': 'ml'},
        {'ingredient_name': 'Avocado Oil',         'category': 'liquids', 'us_quantity': 1,    'us_unit': 'tbsp', 'metric_quantity': 14,  'metric_unit': 'ml'},
        {'ingredient_name': 'Sesame Oil',          'category': 'liquids', 'us_quantity': 1,    'us_unit': 'tbsp', 'metric_quantity': 14,  'metric_unit': 'ml'},
        {'ingredient_name': 'Soy Sauce',           'category': 'liquids', 'us_quantity': 1,    'us_unit': 'tbsp', 'metric_quantity': 15,  'metric_unit': 'ml'},
        {'ingredient_name': 'Lemon Juice',         'category': 'liquids', 'us_quantity': 1,    'us_unit': 'tbsp', 'metric_quantity': 15,  'metric_unit': 'ml'},
        {'ingredient_name': 'Molasses',            'category': 'liquids', 'us_quantity': 1,    'us_unit': 'tbsp', 'metric_quantity': 20,  'metric_unit': 'ml'},

        # Sweeteners
        {'ingredient_name': 'Cane Sugar',          'category': 'sweeteners', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 200, 'metric_unit': 'g'},
        {'ingredient_name': 'Coconut Sugar',       'category': 'sweeteners', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 180, 'metric_unit': 'g'},

        # Nuts & Seeds
        {'ingredient_name': 'Walnuts (chopped)',   'category': 'nuts_seeds', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 120, 'metric_unit': 'g'},
        {'ingredient_name': 'Almonds (whole)',     'category': 'nuts_seeds', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 145, 'metric_unit': 'g'},
        {'ingredient_name': 'Cashews (whole)',     'category': 'nuts_seeds', 'us_quantity': 1, 'us_unit': 'cup', 'metric_quantity': 130, 'metric_unit': 'g'},
        {'ingredient_name': 'Sesame Seeds',        'category': 'nuts_seeds', 'us_quantity': 1, 'us_unit': 'tbsp','metric_quantity': 9,   'metric_unit': 'g'},
        {'ingredient_name': 'Nutritional Yeast',   'category': 'nuts_seeds', 'us_quantity': 1, 'us_unit': 'tbsp','metric_quantity': 5,   'metric_unit': 'g'},

        # Spices
        {'ingredient_name': 'Sea Salt',            'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 6, 'metric_unit': 'g'},
        {'ingredient_name': 'Black Pepper',        'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 2, 'metric_unit': 'g'},
        {'ingredient_name': 'Garlic Powder',       'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 3, 'metric_unit': 'g'},
        {'ingredient_name': 'Smoked Paprika',      'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 2, 'metric_unit': 'g'},
        {'ingredient_name': 'Ground Cumin',        'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 2, 'metric_unit': 'g'},
        {'ingredient_name': 'Ground Cinnamon',     'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 3, 'metric_unit': 'g'},
        {'ingredient_name': 'Ground Turmeric',     'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 3, 'metric_unit': 'g'},
        {'ingredient_name': 'Cayenne Pepper',      'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 2, 'metric_unit': 'g'},
        {'ingredient_name': 'Onion Powder',        'category': 'spices', 'us_quantity': 1, 'us_unit': 'tsp', 'metric_quantity': 2, 'metric_unit': 'g'},
    ]

    def handle(self, *args, **kwargs):
        created_count = 0
        updated_count = 0

        for m in self.MEASUREMENTS:
            obj, created = MeasurementConversion.objects.update_or_create(
                ingredient_name=m['ingredient_name'],
                us_unit=m['us_unit'],
                defaults=m
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {created_count} created, {updated_count} updated'
            )
        )