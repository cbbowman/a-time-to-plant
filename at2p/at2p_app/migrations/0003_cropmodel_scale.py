# Generated by Django 4.1.5 on 2023-01-30 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('at2p_app', '0002_cropmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropmodel',
            name='scale',
            field=models.CharField(default=0, max_length=2, verbose_name='Temperature Scale'),
            preserve_default=False,
        ),
    ]
