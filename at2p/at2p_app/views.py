from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views import generic
from .forms import NewPlanterForm, ProfileForm
from .models import TimeToPlant, Crop, Planter, WeatherInfo, models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from typing import Any, Dict, Optional
import csv


class ImportCrops(generic.base.RedirectView, UserPassesTestMixin):

    def setup(self, request, *args: Any, **kwargs: Any) -> None:
        print(request.method)
        if request.method == 'POST':
            with open('at2p_app/crops_and_temps.csv', encoding='UTF-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    _, created = Crop.objects.get_or_create(
                        name=row[0],
                        min_temp=row[1],
                        min_opt_temp=row[2],
                        max_opt_temp=row[3],
                        max_temp=row[4],
                    )
        return super().setup(request, *args, **kwargs)

    def test_func(self):
        # return self.request.user.username == 'charlie'
        return True

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse_lazy('home')


class Profile(generic.DetailView, LoginRequiredMixin):
    login_url = reverse_lazy('auth')
    model = Planter
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        planter = self.model.objects.get(pk=self.request.user.id)
        context['title'] = planter
        if planter.zip is not None:
            if not WeatherInfo.objects.filter(country=planter.country, zip=planter.zip).exists():
                WeatherInfo.objects.create(
                    country=planter.country, zip=planter.zip)
            w = WeatherInfo.objects.get(
                country=planter.country, zip=planter.zip)
            w.clean()
            w.update_weather()
            context['soil'] = w.historic_avg_temp
            context['high'] = w.forecast_high_temp
            context['low'] = w.forecast_low_temp
            plantings = TimeToPlant.objects.filter(planter=planter.pk)
            for planting in plantings:
                soil_temp_ok = planting.crop.max_opt_temp > w.historic_avg_temp and planting.crop.min_opt_temp < w.historic_avg_temp
                forecast_high_ok = planting.crop.max_temp < w.forecast_high_temp
                forecast_low_ok = planting.crop.min_temp < w.forecast_low_temp
                planting.plantable = soil_temp_ok and forecast_high_ok and forecast_low_ok
            context['plantings'] = plantings
        return context

    def get_object(self) -> models.Model:
        planter = Planter.objects.get(pk=self.request.user.id)
        return planter


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
