from django.contrib.auth.models import AbstractUser
from django.db import models 
from django_countries.fields import CountryField

COUNTRIES_ONLY = ['AD', 'AR', 'AS', 'AT', 'AU', 'AX', 'AZ', 'BD', 'BE', 'BG', 'BM', 'BR', 'BY', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EE', 'ES', 'FI', 'FM', 'FO', 'FR', 'GB', 'GF', 'GG', 'GL', 'GP', 'GT', 'GU', 'HR', 'HT', 'HU', 'IE', 'IM', 'IN', 'IS', 'IT', 'JE', 'JP', 'KR', 'LI', 'LK', 'LT', 'LU', 'LV', 'MC', 'MD', 'MH', 'MK', 'MP', 'MQ', 'MT', 'MW', 'MX', 'MY', 'NC', 'NL', 'NO', 'NZ', 'PE', 'PH', 'PK', 'PL', 'PM', 'PR', 'PT', 'PW', 'RE', 'RO', 'RS', 'RU', 'SE', 'SG', 'SI', 'SJ', 'SK', 'SM', 'TH', 'TR', 'UA', 'US', 'UY', 'VA', 'VI', 'WF', 'YT', 'ZA']

class Planter(AbstractUser):
    country = CountryField(default='US')
    zip = models.CharField(max_length=10, blank=True, null=True)
