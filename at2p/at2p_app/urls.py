from django.urls import path
from at2p_app.views import ImportCrops, Profile, ProfileEdit, Home, Register, Authenticate, Deauthenticate, AuthReset, AuthResetConfirm, AuthResetComplete, AuthResetDone, PassChange, PassChangeDone


urlpatterns = [
    path('import', ImportCrops.as_view(), name='load-crops'),
    path('profile', Profile.as_view(), name='profile'),
    path('profile/edit', ProfileEdit.as_view(), name='profile-edit'),
    path('home', Home.as_view(), name='home'),
    path('register', Register.as_view(), name='register'),
    path('auth', Authenticate.as_view(), name='auth'),
    path('deauth', Deauthenticate.as_view(), name='deauth'),
    path('reset', AuthReset.as_view(), name='auth-reset'),
    path('reset/<uidb64>/<token>', AuthResetConfirm.as_view(), name='auth-reset-confirm'),
    path('reset/complete', AuthResetComplete.as_view(), name='auth-reset-complete'),
    path('reset/done', AuthResetDone.as_view(), name='auth-reset-done'),
    path('change-password', PassChange.as_view(), name='pw-change'),
    path('change-password/done', PassChangeDone.as_view(), name='pw-change-done'),
    path('', Home.as_view(), name='home'),
]
