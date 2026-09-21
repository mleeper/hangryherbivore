from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RecipePage, MeasurementConversion
from .serializers import RecipeSerializer
from wagtail.snippets.views.snippets import SnippetViewSet

class MeasurementConversionAPI(APIView):
    def get(self, request):
        try:
            category = request.query_params.get('category')
            unit = request.query_params.get('unit')
            
            queryset = MeasurementConversion.objects.all()
            
            # Optional filters
            if category:
                queryset = queryset.filter(category=category)
            if unit:
                queryset = queryset.filter(metric_unit=unit)

            conversions = queryset.values(
                'ingredient_name',
                'category',
                'us_quantity',
                'us_unit',
                'metric_quantity',
                'metric_unit',
                'notes'
            ).order_by('category', 'sort_order')

            # Group by category
            grouped = {}
            for item in conversions:
                category_key = item['category']
                if category_key not in grouped:
                    grouped[category_key] = []
                grouped[category_key].append(item)

            return Response({
                'count': queryset.count(),
                'results': grouped
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RecipeListAPI(ListAPIView):
    serializer_class = RecipeSerializer
    pagination_class = None

    def get_queryset(self):
        return RecipePage.objects.live().public().order_by(
            '-first_published_at'
        ).prefetch_related(
            'recipe_ingredients',
            'recipe_ingredients__ingredient',
            'recipe_ingredients__ingredient__ingredient_nutrients',
            'recipe_ingredients__ingredient__ingredient_nutrients__nutrient',
            'steps',
            'recipe_category',
        ).select_related(
            'hero_image',
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })

class RecipeDetailAPI(RetrieveAPIView):
    serializer_class = RecipeSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return RecipePage.objects.live().public().prefetch_related(
            'recipe_ingredients',
            'recipe_ingredients__ingredient',
            'recipe_ingredients__ingredient__ingredient_nutrients',
            'recipe_ingredients__ingredient__ingredient_nutrients__nutrient',
            'steps',
            'recipe_category',
        ).select_related(
            'hero_image',
        )

