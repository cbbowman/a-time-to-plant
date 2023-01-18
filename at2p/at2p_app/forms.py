from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField
from .models import Planter

class NewPlanterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = Planter
        fields = ('username', 'email', 'password1', 'password2')