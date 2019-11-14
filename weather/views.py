from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import City, Result
import requests
from django.conf import settings
from django.core.paginator import Paginator

OBJS_PER_PAGE = 8


def results(request):
    objs = Result.objects.all().order_by('dt')
    paginator = Paginator(objs, OBJS_PER_PAGE)
    page = int(request.GET.get('page', 1))

    page_cnt = paginator.count // OBJS_PER_PAGE
    if page > page_cnt:
        page = page_cnt
    elif page < 1:
        page = 1

    data = paginator.get_page(page)

    context = {
        'title': 'Results',
        'objs': data
    }

    if request.method == 'GET' and request.is_ajax():
        if not len(data.object_list):
            return JsonResponse({'code': '404', 'msg': 'Weather not found'})

        json_data = {
            'code': '200',
            'page_cnt': page_cnt,
            'curr_page': page,
            'items': [d.get_data() for d in data.object_list],
        }
        return JsonResponse(json_data)
    return render(request, 'test.html', context)


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
        res = [Result(city=city, json=r) for r in data['list']]
        Result.objects.bulk_create(res)
        return res

    if request.method == 'GET' and request.is_ajax():
        try:
            city = City.objects.get(id=request.GET.get('city'))
        except City.DoesNotExist:
            return JsonResponse({'code': '404', 'msg': "City not found"})

        weather = get_weather(city.id)
        if int(weather.get('cod')) == 200:
            try:
                results = save_results(city, weather)

                data = []
                dates = sorted(set(r.dt.strftime('%m/%d/%Y') for r in results))

                for date in dates:
                    day = dict(date=date, list=list())

                    for res in results:
                        if res.dt.strftime('%m/%d/%Y') == date:
                            day['list'].append(res.get_data())
                            results.remove(res)
                    day['list'] = sorted(day['list'], key=lambda k: k['time'])

                    data.append(day)

                return JsonResponse({'code': '200', 'items': data})
            except KeyError:
                return JsonResponse({'code': '404', 'msg': 'Weather not found'})
        else:
            return JsonResponse({'code': weather['cod'], 'msg': weather['message']})

    return render(request, 'weather/home.html', context)


def get_city(request):
    if request.is_ajax():
        cities = City.objects.filter(name__icontains=request.GET.get('q[term]'))[:10]
        return JsonResponse({'items': dict((city.id, city.name) for city in cities)})
    else:
        raise Http404
