# Generated by Django 2.2.7 on 2019-11-13 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0009_auto_20191113_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='temp_max',
        ),
        migrations.RemoveField(
            model_name='result',
            name='temp_min',
        ),
    ]