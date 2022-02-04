from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'weather_forecast/index.html')


def get_weather_forecast_request(request, latitude, longitude):
    context = {
        'location': 'ПОКА ПУСТО',
        'latitude': '',
        'longitude': '',
    }
    return render(request, 'weather_forecast/answer.html', context=context)
