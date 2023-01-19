from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, ModelForm
from .models import Planter
import pgeocode
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from . import country_codes
from django_countries import countries


COUNTRIES_ONLY = country_codes.COUNTRIES_ONLY
COUNTRIES_FIRST = ['US']


class NewPlanterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = Planter
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(ModelForm):
    class Meta:
        model = Planter
        fields = ('username', 'country', 'zip')
        widgets = {'country': CountrySelectWidget()}

    def clean(self) -> None:
        n = pgeocode.Nominatim(self.data['country'])
        if self.data['country'] == n.query_postal_code(self.data['zip']).country_code:
            return
        else:
            raise ValidationError(
                "Form error: Country / ZIP combination is invalid.")
