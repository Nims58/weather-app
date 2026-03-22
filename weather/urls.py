from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="weather-dashboard"),
    path("weather/", views.current_weather, name="current-weather"),
]
