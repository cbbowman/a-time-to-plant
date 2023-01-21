# Generated by Django 4.1.5 on 2023-01-20 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('at2p_app', '0002_timetoplant_planter_crops'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planter',
            name='crops',
            field=models.ManyToManyField(blank=True, null=True, through='at2p_app.TimeToPlant', to='at2p_app.crop'),
        ),
    ]