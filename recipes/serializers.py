from rest_framework import serializers
from .models import RecipePage


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = serializers.SerializerMethodField()
    instructions = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()


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
            "calories",
            "protein",
            "carbs",
            "fat",
            "cuisine",
            "category",
            "difficulty",
            "affiliate_product",
            "sponsored",
            "ingredients",
            "instructions",
            "image",
            "first_published_at",
        ]


    def get_ingredients(self, obj):
        return obj.get_schema_ingredients()


    def get_instructions(self, obj):
        return obj.get_schema_instructions()


    def get_image(self, obj):
        if obj.hero_image:
            return obj.hero_image.file.url
        return None

