from django.contrib import admin
from .models import City, Result

# Register your models here.
admin.site.register(City)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    exclude = ('city', )
