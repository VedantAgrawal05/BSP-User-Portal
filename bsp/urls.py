from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
# from .forms import CustomLoginForm
# from .forms import MyAuthForm
# from django.contrib.auth.views import LoginView



app_name = "bsp"
urlpatterns = [
    path("", views.homepage, name="home"),
    path("HR-Dashboard/", views.dept_hr_dashboard, name="hr_dash"),
    path("Admin-Dashboard", views.superuser_dashboard, name="superuser_dash"),
    path("punch/", views.punching_home, name="punch_home"),
    path("punch-in/", views.punch_in, name="punch_in"),
    path("punch-out/", views.punch_out, name="punch_out"),
    path("punch/punches/", views.punch_history, name="punch_log"),



    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    #     path('accounts/login/', LoginView.as_view(
    #     template_name='registration/login.html',
    #     authentication_form=CustomLoginForm,
    # ), name='login'),

    # path('accounts/login/', auth_views.LoginView.as_view(), name='login', kwargs={"authentication_form":CustomAuthForm}),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=MyAuthForm), name='login'),


    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),               #for some reason was not included in default auth configs
    path('accounts/signup/', views.signup, name='signup'),                  #adding(registering) a new user
]