# Generated by Django 2.2.7 on 2019-11-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0010_auto_20191113_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='weather',
            field=models.CharField(default='', max_length=100),
        ),
    ]
