from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views import generic
from .forms import NewPlanterForm, ProfileForm
from .models import Planter
from django.contrib.auth.mixins import LoginRequiredMixin


class Profile(generic.DetailView, LoginRequiredMixin):
    model = Planter
    template_name = 'users/profile.html'

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.id)

class ProfileEdit(generic.UpdateView, LoginRequiredMixin):
    model = Planter
    template_name = 'users/profile_edit.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.id)



class Home(generic.base.TemplateView):
    template_name = 'home.html'


class Register(generic.CreateView):
    title = 'Register'
    form_class = NewPlanterForm
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
    template_name = 'users/auth_reset_form.html'
    email_template_name = 'users/reset_email.html'
    success_url = reverse_lazy('auth-reset-done')


class AuthResetConfirm(PasswordResetConfirmView):
    template_name = 'users/auth_reset_confirm.html'


class AuthResetComplete(PasswordResetCompleteView):
    pass


class AuthResetDone(PasswordResetDoneView):
    template_name = 'users/auth_reset_done.html'


class PassChange(PasswordChangeView):
    pass


class PassChangeDone(PasswordChangeDoneView):
    pass
