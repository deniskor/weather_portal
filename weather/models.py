from django.db import models
from datetime import datetime


# Create your models here.
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name.capitalize()


class Result(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    dt = models.DateTimeField()
    temp = models.FloatField(default=0)
    clouds = models.IntegerField(default=0)
    wind = models.FloatField(default=0)
    weather = models.CharField(max_length=100, default='')

    def __init__(self, *args, **kwargs):
        if 'json' in kwargs:
            json_dict = kwargs.pop('json')
            parsed_json = {
                'dt': datetime.fromtimestamp(json_dict['dt']),
                'temp': json_dict['main']['temp'],
                'clouds': json_dict['clouds']['all'],
                'wind': json_dict['wind']['speed'],
                'weather': " / ".join(x['main'] for x in json_dict['weather']),
            }
            kwargs.update(parsed_json)
        super(Result, self).__init__(*args, **kwargs)

    def get_data(self, time_format='%H:%M'):
        data = {
            'time': self.dt.strftime(time_format),
            'temp': round(self.temp),
            'clouds': self.clouds,
            'wind': self.wind,
            'city': self.city.name,
            'weather': self.weather,
        }
        return data

    def __str__(self):
        return self.dt.strftime("%m/%d/%Y, %H:%M:%S")
