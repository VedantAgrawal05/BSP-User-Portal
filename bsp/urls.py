from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .forms import CustomLoginForm
from django.contrib.auth.views import LoginView



app_name = "bsp"
urlpatterns = [
    path("", views.homepage, name="home"),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
        path('accounts/login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomLoginForm,
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),               #for some reason was not included in default auth configs
    path('accounts/signup/', views.signup, name='signup'),                  #adding(registering) a new user
]