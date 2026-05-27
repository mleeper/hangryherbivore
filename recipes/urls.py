from django.urls import path
from recipes.views import RecipeListAPI, RecipeDetailAPI


urlpatterns = [
    path("api/recipes/", RecipeListAPI.as_view()),
    path("api/recipes/<slug:slug>/", RecipeDetailAPI.as_view()),
]
