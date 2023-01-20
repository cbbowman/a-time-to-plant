from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, ModelForm
from .models import Planter, Crop
import pgeocode
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from . import country_codes
from django_countries import countries


COUNTRIES_ONLY = country_codes.COUNTRIES_ONLY
COUNTRIES_FIRST = ['US']


class NewCropForm(ModelForm):
    class Meta:
        model = Crop
        fields = ('name', 'min_temp', 'min_opt_temp',
                  'max_opt_temp', 'max_temp', 'slug')
        widgets = {'country': CountrySelectWidget()}


class NewPlanterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = Planter
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = Planter
        fields = ('username', 'country', 'zip', 'crops')
        widgets = {'country': CountrySelectWidget()}

    def clean(self) -> None:
        n = pgeocode.Nominatim(self.data['country'])
        country = n.query_postal_code(self.data['zip']).country_code
        if self.data['country'] == country:
            return
        else:
            raise ValidationError(
                "Form error: Country / ZIP combination is invalid.")
