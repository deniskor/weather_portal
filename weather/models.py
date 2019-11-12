from django.db import models
from datetime import datetime


# Create your models here.
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name.capitalize()


class Result(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temp = models.FloatField(default=0)
    clouds = models.IntegerField(default=0)
    wind = models.FloatField(default=0)

    def __init__(self, *args, **kwargs):
        if 'json' in kwargs:
            json_dict = kwargs.pop('json')
            parsed_json = {
                'timestamp': datetime.fromtimestamp(json_dict['dt']),
                'temp': json_dict['main']['temp'],
                'clouds': json_dict['clouds']['all'],
                'wind': json_dict['wind']['speed'],
            }
            kwargs.update(parsed_json)
        super(Result, self).__init__(*args, **kwargs)

    # def __str__(self):
    #     return self.time.strftime("%m/%d/%Y, %H:%M:%S")
