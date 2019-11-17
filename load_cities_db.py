import json
from weather.models import City
from datetime import datetime

# Read json list of cities
with open('city.list.json', 'rb') as f:
    print(datetime.now(), 'Reading json')
    data = json.load(f)
    print(datetime.now(), 'File has been read')

print(datetime.now(), 'Creating city objects')
cities = [City(id=d['id'], name=f"{d['name']}| {d['country']}") for d in data]
print(datetime.now(), 'Creating has been finished', 'Number of objects:', len(cities))

print(datetime.now(), 'Saving cities in db')
City.objects.bulk_create(cities)
print(datetime.now(), 'Cities have been saved', 'Number of stored cities:', City.objects.count())
