# Generated by Django 4.1.6 on 2023-02-04 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('at2p_app', '0007_placemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='placemodel',
            name='weather_id',
            field=models.UUIDField(default=0, verbose_name='Weather ID'),
            preserve_default=False,
        ),
    ]
