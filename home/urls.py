from django.urls import path
from home.views import HomePageAPI, AboutPageAPI


urlpatterns = [
    path("api/home/", HomePageAPI.as_view()),
    path("api/about/", AboutPageAPI.as_view()),
]
