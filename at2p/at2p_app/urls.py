from django.urls import path
from at2p_app.views import Home, Register, Authenticate, Deauthenticate, AuthReset, AuthResetConfirm, AuthResetComplete, AuthResetDone, PassChange, PassChangeDone


urlpatterns = [
    path('home', Home.as_view(), name='home'),
    path('register', Register.as_view(), name='register'),
    path('auth', Authenticate.as_view(), name='auth'),
    path('deauth', Deauthenticate.as_view(), name='deauth'),
    path('reset', AuthReset.as_view(), name='auth-reset'),
    path('reset/confirm', AuthResetConfirm.as_view(), name='auth-reset-confirm'),
    path('reset/complete', AuthResetComplete.as_view(), name='auth-reset-complete'),
    path('reset/done', AuthResetDone.as_view(), name='auth-reset-done'),
    path('change-password', PassChange.as_view(), name='pw-change'),
    path('change-password/done', PassChangeDone.as_view(), name='pw-change-done'),
    path('', Home.as_view(), name='home'),
]
