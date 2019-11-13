# Generated by Django 2.2.7 on 2019-11-13 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0008_auto_20191111_1451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='timestamp',
            new_name='dt',
        ),
        migrations.AddField(
            model_name='result',
            name='temp_max',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='temp_min',
            field=models.FloatField(default=0),
        ),
    ]
