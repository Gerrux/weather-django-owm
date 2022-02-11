from django.shortcuts import render
from django.http import HttpResponseRedirect
from .wfbOWM import get_information_about_weather_forecast as wf


# Create your views here.


def index(request):
    """
    Функция возвращает главную страницу сайта
    :param request:
    :return: render
    """
    return render(request, 'weather_forecast/index.html')


def get_weather_forecast_by_location(request, location: str):
    """
    Функция возвращает страницу ответа на запрос прогноза погоды по локации
    :param request:
    :param location: An string
    :return: HttpResponseRedirect
    """
    context = {
        'location': location,
        'weather_forecast': wf(location),
    }
    return render(request, 'weather_forecast/answer.html', context=context)


def get_redirect_by_result(request):
    """
    Функция перенаправляет на выполнение запроса по локации
    :param request:
    :return: HttpResponseRedirect
    """
    location = request.GET.get("location")
    return HttpResponseRedirect(f"/{location}")


def get_weather_forecast_by_coordinates(request, latitude: float, longitude: float):
    """
    Функция возвращает страницу ответа на запрос прогноза погоды по координатам
    :param request:
    :param latitude:
    :param longitude:
    :return: HttpResponseRedirect
    """
    context = {
        'location': 'ПОКА ПУСТО',
        'latitude': '',
        'longitude': '',
    }
    return render(request, 'weather_forecast/answer.html', context=context)
