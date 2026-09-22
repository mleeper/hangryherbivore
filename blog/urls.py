from django.urls import path
from .views import BlogListAPI, BlogDetailAPI, BlogCategoryListAPI

urlpatterns = [
    path('api/blog/', BlogListAPI.as_view()),
    path('api/blog/categories/', BlogCategoryListAPI.as_view()),
    path('api/blog/<slug:slug>/', BlogDetailAPI.as_view()),
]