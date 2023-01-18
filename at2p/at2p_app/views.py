from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views import generic


class Home(generic.base.TemplateView):
    template_name = 'home.html'


class Register(generic.CreateView):
    title = 'Register'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'users/register.html'


class Authenticate(LoginView):
    redirect_authenticated_user = True
    title = 'Auth'
    template_name = 'users/auth.html'

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class Deauthenticate(LogoutView):
    next_page = reverse_lazy('home')

class AuthReset(PasswordResetView):
    pass


class AuthResetConfirm(PasswordResetConfirmView):
    pass


class AuthResetComplete(PasswordResetCompleteView):
    pass


class AuthResetDone(PasswordResetDoneView):
    pass


class PassChange(PasswordChangeView):
    pass


class PassChangeDone(PasswordChangeDoneView):
    pass
