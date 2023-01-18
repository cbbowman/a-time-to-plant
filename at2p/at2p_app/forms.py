from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField

class NewUserForm(UserCreationForm):
    email = EmailField()