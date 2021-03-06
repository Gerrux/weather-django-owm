from django.urls import path, register_converter
from . import views, converters

register_converter(converters.DegreesConverter, 'degrees')

urlpatterns = [
    path('', views.index),
    path('result', views.get_redirect_by_result, name='forecast_request'),
    path('<degrees:latitude>/<degrees:longitude>/', views.get_weather_forecast_by_coordinates),
    path('<str:location>/', views.get_weather_forecast_by_location, name='forecast_by_location')
]
