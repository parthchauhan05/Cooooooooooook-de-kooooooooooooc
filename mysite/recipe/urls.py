from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url("accounts/", include("django.contrib.auth.urls")),
    path('', views.index, name='index'),
    path('accounts/sign_up/',views.sign_up,name="sign-up"),
    path('accounts/log_in/',views.log_in,name="log-in"),
    path('accounts/log_out/',views.log_out,name="log-out"),
]