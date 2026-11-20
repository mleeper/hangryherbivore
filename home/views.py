from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HomePage, AboutPage
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

            # CTA Links
            'hero_cta__link',
            'how_it_works_cta__link',
            'about_cta__link',
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

class AboutPageAPI(APIView):
    def get(self, request):
        page = AboutPage.objects.live().first()
        if not page:
            return Response({"error": "Not found"}, status=404)
        return Response({
            "title": page.title,
            "intro": page.intro,
            "body": page.body,   # rich text; consider rich text rendering if you embed links
            "hero_image": page.hero_image.file.url if page.hero_image else None,
            "meta": {
                "seo_title": page.seo_title or page.title,
                "search_description": (page.search_description or page.intro)[:160],
            },
        })