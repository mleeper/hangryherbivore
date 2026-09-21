from rest_framework import serializers
from .models import RecipePage


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = serializers.SerializerMethodField()
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

