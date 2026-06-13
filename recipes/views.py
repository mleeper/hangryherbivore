from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import RecipePage
from .serializers import RecipeSerializer


class RecipeListAPI(ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):	
        return RecipePage.objects.all().prefetch_related(
            'recipe_ingredients__ingredient__ingredient_nutrients__nutrient'
        )	
        #return RecipePage.objects.all().live().specific()
        #return RecipePage.objects.live().public()

class RecipeDetailAPI(RetrieveAPIView):
    serializer_class = RecipeSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return RecipePage.objects.live().public()

