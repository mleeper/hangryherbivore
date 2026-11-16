from rest_framework import serializers
from .models import RecipePage

CORE = {"Calories", "Protein", "Carbohydrates", "Total Fat", "Fiber", "Sodium"}

class RecipeSerializer(serializers.ModelSerializer):

    ingredients = serializers.SerializerMethodField()
    nutrition = serializers.SerializerMethodField()
    instructions = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = RecipePage
        fields = [
            "title",
            "slug",
            "description",
            "prep_time",
            "cook_time",
            "total_time",
            "servings",
            "cost_per_serving",
            "category",
            "difficulty",
            "affiliate_product",
            "sponsored",
            "ingredients",
            "nutrition",
            "instructions",
            "image",
            "first_published_at",
            "meta",
        ]


    def get_ingredients(self, obj):
        return obj.get_schema_ingredients()


    def get_instructions(self, obj):
        return obj.get_schema_instructions()


    def get_image(self, obj):
        if obj.hero_image:
            return obj.hero_image.file.url
        return None
    
    def get_category(self, obj):
        return obj.get_schema_categories()

    def get_meta(self, obj):
        description = obj.search_description or obj.description or ''
        return {
            'seo_title': obj.seo_title or obj.title,
            'search_description': description[:160],  # trim for meta tag
            'slug': obj.slug,
            'first_published_at': obj.first_published_at,
            'last_published_at': obj.last_published_at,
        }

    def get_nutrition(self, obj):
        servings = obj.servings or 1
        rows = []
        for name, v in obj.get_recipe_total_nutrition().items():
            per = round(v["amount"] / servings, 1)
            if per == 0 and name not in CORE:
                continue
            rows.append({"name": name, "unit": v["unit"], "per_serving": per})
        return rows

