# Generated by Django 4.1.5 on 2023-02-02 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('at2p_app', '0003_cropmodel_scale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cropmodel',
            name='scale',
        ),
    ]
