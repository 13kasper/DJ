from django.shortcuts import render
import requests
from .models import City


def weather(request):
    app_id = 'dd3acb1b7cb94eef8ca175721220206'
    cities = City.objects.all()

    all_cities = []
    for city in cities:
        url = f'http://api.weatherapi.com/v1/current.json?key={app_id}&q={city.name}&aqi=no'
        res = requests.get(url).json()

        city_info = {
            'city': city.name,
            'temp': res['current']['temp_c'],
            'icon': res['current']['condition']['icon']
        }

        all_cities.append(city_info)

    context = {
        'all_info': all_cities
    }

    return render(request, template_name='weather/weather.html', context=context)
