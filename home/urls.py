from django.urls import path
from home.views import HomePageAPI


urlpatterns = [
    path("api/home/", HomePageAPI.as_view()),
]
