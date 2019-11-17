from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import City, Result
import requests
from django.conf import settings
from django.core.paginator import Paginator
from datetime import datetime
from functools import wraps

OBJS_PER_PAGE = 12


def results(request):
    def build_raw_query(start, end=''):
        def dec_outer(fn):
            @wraps(fn)
            def dec_inner(*args, **kwargs):
                return f"""{start} {fn(args[0]) if args[0] else ''} {end}"""
            return dec_inner
        return dec_outer

    @build_raw_query('SELECT * FROM weather_result', 'ORDER BY dt;')
    def params(filter_by):
        return "WHERE " + " AND ".join(f'''{v['param']}{v['op']}%({k})s''' for k, v in filter_by.items())

    context = {
        'title': 'Results'
    }

    if request.method == 'GET' and request.is_ajax():
        # query_params = dict(city_id=request.GET.get('city'),
        #                       dt__gte=request.GET.get('from'),
        #                       dt__lte=request.GET.get('to'))
        #
        # filter_by = {k: v for k, v in query_params.items() if v}
        # objs = Result.objects.filter(**filter_by).order_by('dt')

        query_params = dict(
            city_id={'value': request.GET.get('city'), 'param': 'city_id', 'op': '='},
            dt_since={'value': request.GET.get('from'), 'param': 'dt', 'op': '>='},
            dt_until={'value': request.GET.get('to'), 'param': 'dt', 'op': '<='},
        )
        filter_by = {k: v for k, v in query_params.items() if v['value']}
        query = params(filter_by)

        objs = Result.objects.raw(query, {k: v['value'] for k, v in filter_by.items()})
        paginator = Paginator(objs, OBJS_PER_PAGE)
        page = int(request.GET.get('page', 1))

        page_cnt = paginator.num_pages
        if page > page_cnt:
            page = page_cnt
        elif page < 1:
            page = 1

        data = paginator.get_page(page)

        if not len(data.object_list):
            return JsonResponse({'code': '404', 'msg': 'Weather not found'})

        json_data = {
            'code': '200',
            'page_cnt': page_cnt,
            'curr_page': page,
            'items': [d.get_data('%m-%d-%Y %H:%M') for d in data.object_list],
        }
        return JsonResponse(json_data)
    return render(request, 'weather/results.html', context)


def home_page(request):
    context = {
        'title': 'Find',
    }

    def get_weather(city_id):
        r = f'https://api.openweathermap.org/data/2.5/forecast?id={city_id}' \
            f'&APPID={settings.OPEN_WEATHER_API_TOKEN}&units=metric'

        return requests.get(r).json()

    def save_results(city, data):
        # Filter and deleting old results with the same date and city
        timestamps = [datetime.fromtimestamp(x) for x in set(x['dt'] for x in data['list'])]
        Result.objects.filter(dt__in=timestamps, city=city).delete()

        # Create and save results
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

                # Group by days
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
        cities = City.objects.filter(name__istartswith=request.GET.get('q[term]')).order_by('name')[:10]
        return JsonResponse({'items': dict((city.id, city.name) for city in cities)})
    else:
        raise Http404
