from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost, BlogIndexPage, BlogCategory


class BlogListAPI(APIView):
    def get(self, request):
        try:
            category = request.query_params.get('category')
            tag = request.query_params.get('tag')

            posts = BlogPost.objects.live().public().order_by(
                '-first_published_at'
            ).prefetch_related('categories', 'tags')

            # Apply filters
            if category:
                posts = posts.filter(categories__slug=category)
            if tag:
                posts = posts.filter(tags__slug=tag)

            data = []
            for post in posts:
                data.append({
                    'id': post.id,
                    'title': post.title,
                    'slug': post.slug,
                    'excerpt': post.excerpt,
                    'first_published_at': post.first_published_at,
                    'hero_image': post.hero_image.get_rendition(
                        'fill-800x450'
                    ).url if post.hero_image else None,
                    'categories': [
                        {
                            'name': cat.name,
                            'slug': cat.slug,
                            'icon': cat.icon,
                        }
                        for cat in post.categories.all()
                    ],
                    'tags': [
                        {
                            'name': tag.name,
                            'slug': tag.slug,
                        }
                        for tag in post.tags.all()
                    ],
                })

            return Response({
                'count': len(data),
                'results': data
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BlogDetailAPI(APIView):
    def get(self, request, slug):
        try:
            post = BlogPost.objects.live().public().prefetch_related(
                'categories', 'tags'
            ).get(slug=slug)

            # Get related posts by shared category
            related = BlogPost.objects.live().public().filter(
                categories__in=post.categories.all()
            ).exclude(id=post.id).distinct().order_by(
                '-first_published_at'
            )[:3]

            data = {
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'excerpt': post.excerpt,
                'content': post.content,
                'first_published_at': post.first_published_at,
                'last_published_at': post.last_published_at,
                'hero_image': post.hero_image.get_rendition(
                    'fill-1200x600'
                ).url if post.hero_image else None,
                'categories': [
                    {
                        'name': cat.name,
                        'slug': cat.slug,
                        'icon': cat.icon,
                        'description': cat.description,
                    }
                    for cat in post.categories.all()
                ],
                'tags': [
                    {
                        'name': tag.name,
                        'slug': tag.slug,
                    }
                    for tag in post.tags.all()
                ],
                'related_posts': [
                    {
                        'title': r.title,
                        'slug': r.slug,
                        'excerpt': r.excerpt,
                        'hero_image': r.hero_image.get_rendition(
                            'fill-400x225'
                        ).url if r.hero_image else None,
                    }
                    for r in related
                ]
            }

            return Response(data)

        except BlogPost.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BlogCategoryListAPI(APIView):
    """Returns all blog categories with post counts"""
    def get(self, request):
        try:
            from django.db.models import Count
            categories = BlogCategory.objects.annotate(
                post_count=Count('posts')
            ).order_by('sort_order', 'name')

            data = [
                {
                    'name': cat.name,
                    'slug': cat.slug,
                    'icon': cat.icon,
                    'description': cat.description,
                    'post_count': cat.post_count,
                }
                for cat in categories
            ]

            return Response({
                'count': len(data),
                'results': data
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )