# recipes/management/commands/import_recipes.py
import os
from pathlib import Path
import json
import difflib
from wagtail.models import Page
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, RecipePage, RecipeIngredient
from recipes.utils.converter import convert_raw_line
from recipes.utils.closest_match import find_closest_match_levenshtein, match_ingredient
from recipes.utils.find_index_lowercase import find_index_lowercase

class Command(BaseCommand):
    help = "Import recipes"

    def handle(self, *args, **kwargs):
        path = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'recipes' / 'original'
        converted_path = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'recipes' / 'converted'
        missing_ingredients_path = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'recipes' / 'missing_ingredients.json'
        files = [file.name for file in path.iterdir() if file.is_file()]
        
        ingredients = Ingredient.objects.all()
        recipes = RecipePage.objects.all()
        recipe_names = []
        ingredient_names = []
        missing_ingredients = []

        root_page = Page.objects.get(id=33)

        for rp in recipes:
            recipe_names.append(rp.title)
        
        for ing in ingredients:
            ingredient_names.append(ing.name)

        for file in files:
            with open(path / file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # Convert Recipe to metric weight
            converted_lines = []
            for line in lines:
                converted_line = convert_raw_line(line)
                converted_lines.append(converted_line)
            
            # Extract Name
            name_array = [item for item in converted_lines if isinstance(item, dict) and item.get('Name') != None][0]
            name = name_array.get('Name')
            
            # Normalize for case
            recipe_name_index = find_index_lowercase(recipe_names, name)
            matched_recipe_name = recipe_names[recipe_name_index] if recipe_name_index >=0 else name
            slug = matched_recipe_name.lower().replace(' ', '-')

            recipe_page = None
            # Check if a page with the same slug exists under the same parent
            recipe_exists = root_page.get_children().filter(slug=slug).exists()
            if not recipe_exists:
                recipe_page = RecipePage(
                    title = matched_recipe_name,
                    slug = slug
                )
                root_page.add_child(instance=recipe_page)
            else:
                recipe_page = RecipePage.objects.get(slug=slug)

            # Clear existing ingredients before reimporting
            RecipeIngredient.objects.filter(page_id=recipe_page.id).delete()
            
            for line in converted_lines:
                if isinstance(line, dict) and line.get('ingredient') != None:
                    # Check for notes
                    note = ''
                    if line.get('is_note'):
                        note = line.get('ingredient')
                        RecipeIngredient.objects.create(
                            page=recipe_page,
                            note=note
                        )
                    else:
                        # Attach ingredients to recipe
                        matched_ingredient_name = match_ingredient(line.get('ingredient'), ingredient_names)
                        if matched_ingredient_name == None:
                            missing_ingredients.append({ "name" : line.get('ingredient'), "recipe": matched_recipe_name })
                        else:
                            ingredient = Ingredient.objects.get(name = matched_ingredient_name[0])
                            RecipeIngredient.objects.create(
                                page=recipe_page,
                                ingredient=ingredient,
                                unit=line.get('unit'),
                                quantity=line.get('amount')
                            )
           
            # After all ingredients are created for this recipe
            recipe_page.save_revision().publish()
            self.stdout.write(f'✓ Published: {recipe_page.title}')

        # Write recipe to text file
        if(len(missing_ingredients) > 0):
            with open(missing_ingredients_path , "w", encoding="utf-8") as f:
                json.dump(missing_ingredients, f, indent=4)
            
