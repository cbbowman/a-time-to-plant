import csv
from typing import Any, Dict, Optional
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic
from .forms import NewPlanterForm, ProfileForm, NewCropForm
from .models import TimeToPlant, Crop, Planter, WeatherInfo


class CropView(generic.DetailView):
    model = Crop
    template_name = 'crop_detail.html'

    # def get_object(self) -> model:
    #     planter = Crop.objects.get()
    #     return planter


class CropAdd(generic.CreateView):
    title = 'New Crop'
    form_class = NewCropForm
    success_url = reverse_lazy('home')
    template_name = 'crop_create_form.html'


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
                        slug=slugify(row[0])
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
        if planter.zip is None:
            return context

        if not WeatherInfo.objects.filter(country=planter.country,
                                          zip=planter.zip).exists():
            WeatherInfo.objects.create(
                country=planter.country, zip=planter.zip)
        w = WeatherInfo.objects.get(
            country=planter.country, zip=planter.zip)
        w.clean()
        w.update_weather()

        plantings = TimeToPlant.objects.filter(planter=planter.pk)
        for p in plantings:
            p.update_plantable(w)

        context['soil'] = w.historic_avg_temp
        context['high'] = w.forecast_high_temp
        context['low'] = w.forecast_low_temp
        context['plantings'] = plantings.order_by('-plantable_score')
        return context

    def get_object(self) -> Planter:
        planter = Planter.objects.get(pk=self.request.user.id)
        return planter


class ProfileEdit(generic.UpdateView, LoginRequiredMixin):
    model = Planter
    template_name = 'users/profile_edit.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self) -> Planter:
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
