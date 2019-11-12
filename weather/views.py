from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.core import serializers
from .models import City, Result
import requests
import json
from django.conf import settings


# Create your views here.
# def home_page(request, e):
#     context = {
#         'title': 'Home page',
#     }
#
#     return render(request, 'weather/home.html', context)


def find_view(request):
    context = {
        'title': 'Find'
    }
    return render(request, 'base.html', context)


def history_view(request):
    context = {
        'title': 'History'
    }
    return render(request, 'base.html', context)


def home_page(request):
    context = {
        'title': 'Find',
    }

    def get_weather(city_id):
        r = f'https://api.openweathermap.org/data/2.5/forecast?id={city_id}' \
            f'&APPID={settings.OPEN_WEATHER_API_TOKEN}&units=metric'

        return requests.get(r).json()

    def save_results(city, data):
        try:
            res = [Result(city=city, json=r) for r in data['list']]
            Result.objects.bulk_create(res)
            return res
        except KeyError:
            raise KeyError

    if request.method == 'GET' and request.is_ajax():
        try:
            city = City.objects.get(id=request.GET.get('city'))
        except City.DoesNotExist:
            return JsonResponse({'code': 404, 'msg': "city doesn't exist"})

        weather = get_weather(city.id)
        if int(weather.get('cod')) == 200:
            try:
                results = save_results(city, weather)
                data = serializers.serialize('json', results)
                return JsonResponse({'list': data})
            except KeyError:
                return JsonResponse({'code': 404, 'msg': 'Results not found'})
        else:
            return JsonResponse({'code': weather['cod'], 'msg': weather['message']})

    return render(request, 'test.html', context)


def get_city(request):
    if request.is_ajax():
        cities = City.objects.filter(name__icontains=request.GET.get('q[term]'))[:10]
        return JsonResponse({'items': dict((city.id, city.name) for city in cities)})
    else:
        raise Http404
