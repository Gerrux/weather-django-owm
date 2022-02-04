from django.urls import path, register_converter
from . import views, converters

register_converter(converters.DegreesConverter, 'degrees')

urlpatterns = [
    path('', views.index),
    path('<degrees:latitude>/<degrees:longitude>/', views.get_weather_forecast_request)
]