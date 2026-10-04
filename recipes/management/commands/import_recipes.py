# recipes/management/commands/import_recipes.py
import os
from pathlib import Path
import json
import difflib
from wagtail.models import Page
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, RecipePage, RecipeIngredient
from recipes.utils.converter import convert_raw_line
from recipes.utils.closest_match import find_closest_match_levenshtein
from recipes.utils.find_index_lowercase import find_index_lowercase

class Command(BaseCommand):
    help = "Import recipes"

    def handle(self, *args, **kwargs):
        path = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'recipes' / 'original'
        files = [file.name for file in path.iterdir() if file.is_file()]
        
        ingredients = Ingredient.objects.all()
        recipes = RecipePage.objects.all()
        recipe_names = []
        
        root_page = Page.objects.get(id=3)

        for rp in recipes:
            recipe_names.append(rp.title)
        
        print(recipe_names)
        for file in files:
            with open(path / file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            converted_lines = []
            for line in lines:
                converted_line = convert_raw_line(line)
                converted_lines.append(converted_line)
            
            name_array = [item for item in converted_lines if isinstance(item, dict) and item.get('Name') != None][0]
            name = name_array.get('Name')
            recipe_name_index = find_index_lowercase(recipe_names, name)
            matched_recipe_name = recipe_names[recipe_name_index] if recipe_name_index >=0 else name
            slug = matched_recipe_name.lower().replace(' ', '-')
            # matched_name = find_closest_match_levenshtein(name, recipe_names)
            

            # Check if a page with the same slug exists under the same parent
            recipe_exists = root_page.get_children().filter(slug=slug).exists()
            print(name, matched_recipe_name, recipe_exists)
            if(not recipe_exists):
                recipe_page = RecipePage(
                    title = matched_recipe_name,
                    slug = slug
                )
                root_page.add_child(instance=recipe_page)
                root_page.save()