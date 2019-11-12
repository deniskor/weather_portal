from .models import City
from django_select2.forms import Select2Widget
from django import forms


class CityWeatherForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=Select2Widget)

