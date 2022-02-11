import pyowm
from pyowm.utils.config import get_default_config
import datetime
import requests
import json

API_KEY_OWM = '0156c6bdea552ac5f63266f2e501af01'

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM(API_KEY_OWM, config_dict)
mgr = owm.weather_manager()


def wind_direction(wind: float):
    """Функция вычисляет сторону света для направления ветра"""
    direction = ''
    deg = float(wind)
    if 0 <= deg < 22.5 or 337.5 < deg <= 360:
        direction = 'север'
    elif 22.5 < deg < 67.5:
        direction = 'северо-восток'
    elif 67.5 < deg < 112.5:
        direction = 'восток'
    elif 112.5 < deg < 157.5:
        direction = 'юго-восток'
    elif 157.5 < deg < 202.5:
        direction = 'юг'
    elif 202.5 < deg < 247.5:
        direction = 'юго-запад'
    elif 247.5 < deg < 292.5:
        direction = 'запад'
    elif 292.5 < deg < 337.5:
        direction = 'северо-запад'
    return direction


def get_information_about_weather_forecast(place="Москва") -> dict:
    """
    Функция выполняет API запрос на OpenWeatherMap и собирает словарь с данными.

    :param place: An string

    :rtype: dict
    :return: answer
    """
    observation = mgr.weather_at_place(place)
    lat = round(observation.location.lat, 4)
    lon = round(observation.location.lon, 4)
    w = observation.weather

    temp = w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}  # 1

    wind = w.wind()  # {'speed': 4.6, 'deg': 330}
    speed_wind = str(round(wind['speed'], 1))  # 2

    direction = wind_direction(wind['deg'])  # 3

    humidity = str(w.humidity)  # 4

    detailed_status = w.detailed_status.split(' ')
    detailed_status[0] = detailed_status[0].title()
    detailed_status = ' '.join(detailed_status)  # 5

    pressure = str(round(float(w.pressure['press']) * 0.750064))  # 6

    icon_name = f'img/{w.weather_icon_name}.png'  # 7

    day_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресение']  # 8

    date = str(datetime.date.today().strftime('%d.%m.%Y')) # 9

    answer = {
        "current_weather": {
            "location": place,
            "latitude": lat,
            "longitude": lon,
            "temp": str(round(temp['temp'], 1)) + '°C',
            "speed_wind": speed_wind,
            "direction_wind": direction,
            "humidity": humidity,
            "detailed_status": detailed_status,
            "pressure": pressure,
            "icon_name": icon_name,
            "day_of_week": day_of_week[datetime.datetime.today().isoweekday() - 1],
            "date": date,
        },
        "weather_forecast": forecast_weather(place)
    }

    return answer


def forecast_weather(place="Москва") -> dict:
    """
    Функция выполняет API запрос на OpenWeatherMap и собирает словарь
    с данными прогноза погоды на ближающую неделю.

    :param place: An string
    :return: forecast_weather_answer an dict
    """
    observation = mgr.weather_at_place(place)
    lat = round(observation.location.lat, 2)
    lon = round(observation.location.lon, 2)
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,current,minutely,alerts&appid={API_KEY_OWM}&lang=ru&units=metric"
    print(url)
    request = requests.get(url)
    forecast = json.loads(request.content)

    forecast_weather_answer = {
    }
    daily_name = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for i in range(1, 8):
        forecast_weather_answer[i] = {
            'temp': round(forecast['daily'][i]['temp']['day'], 1),
            'speed_wind': str(round(forecast['daily'][i]['wind_speed'], 1)),
            'direction_wind': wind_direction(forecast['daily'][i]['wind_deg']),
            'humidity': forecast['daily'][i]['humidity'],
            'detailed_status': forecast['daily'][i]['weather'][0]['description'],
            'pressure': forecast['daily'][i]['pressure'],
            'data_icon': f"img/{forecast['daily'][i]['weather'][0]['icon']}.png",
            'daily_name': daily_name[(datetime.datetime.today().isoweekday() - 1 + i) % 7],
            'daily_date': (datetime.datetime.today() + datetime.timedelta(days=i+1)).strftime("%Y-%m-%d")
        }

    return forecast_weather_answer
