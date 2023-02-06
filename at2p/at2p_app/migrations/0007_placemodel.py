# Generated by Django 4.1.6 on 2023-02-04 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('at2p_app', '0006_alter_cropmodel_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceModel',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, verbose_name='Place ID')),
                ('zip_code', models.CharField(max_length=32, verbose_name='ZIP Code')),
                ('country', models.CharField(max_length=2, verbose_name='Country')),
            ],
        ),
    ]