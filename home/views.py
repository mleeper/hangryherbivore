from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import HomePage
from .serializers import HomeSerializer


class HomePageAPI(ListAPIView):
    serializer_class = HomeSerializer

    def get_queryset(self):	
        return HomePage.objects.all().prefetch_related(
            # Value bar items
            'homepage_value_bar',
            'homepage_value_bar__value_bar_item',

            # How it works items
            'how_it_works_list',
            'how_it_works_list__how_it_works_item',

            # CTA relations
            'hero_cta',
            'how_it_works_cta',
            'about_cta',
        ).select_related(
            # Hero image
            'hero_image',
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })