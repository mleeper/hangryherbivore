from rest_framework import serializers
from .models import HomePage


class HomeSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()
    hero_cta = serializers.SerializerMethodField()
    value_bar = serializers.SerializerMethodField()
    how_it_works_list = serializers.SerializerMethodField()
    how_it_works_cta = serializers.SerializerMethodField()
    about_cta = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = [
            "hero_title",
            "hero_image",
            "hero_subtitle",
            "hero_cta",
            "value_bar",
            "categories",
            "how_it_works_title",
            "how_it_works_text",
            "how_it_works_list",
            "how_it_works_cta",
            "about_title",
            "about_content",
            "about_cta",
            "email_signup_title",
            "email_signup_button_text",
            "email_signup_content",
        ]

    def get_hero_image(self, obj):
        if obj.hero_image:
            return obj.hero_image.file.url
        return None
    
    def get_categories(self, obj):
        return obj.get_schema_categories()
    
    def get_hero_cta(self, obj):
        return obj.get_schema_hero_cta()
    
    def get_how_it_works_cta(self, obj):
        return obj.get_schema_how_it_works_cta()

    def get_about_cta(self, obj):
        return obj.get_schema_about_cta()
    
    def get_how_it_works_list(self, obj):
        return obj.get_schema_how_it_works_list()

    def get_value_bar(self, obj):
        return obj.get_schema_value_bar()
    
    def get_categories(self, obj):
        return obj.get_schema_categories()


