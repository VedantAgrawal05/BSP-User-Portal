from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
# from .forms import CustomLoginForm
# from .forms import MyAuthForm
# from django.contrib.auth.views import LoginView



app_name = "bsp"
urlpatterns = [
    path("home/", views.homepage, name="home"),
    path("HR-Dashboard/", views.dept_hr_dashboard, name="hr_dash"),
    path("Admin-Dashboard", views.superuser_dashboard, name="superuser_dash"),
    path("punch-in/", views.punch_in, name="punch_in"),
    path("punch-out/", views.punch_out, name="punch_out"),
    path("user-punches/", views.punch_history, name="punch_log"),
    path("user-attendance/", views.attendance_history, name="attendance_hist"),
    path("HR-Dashboard/dept-employees/", views.show_dept_users, name="dept_users"),
    path("HR-Dashboard/dept-pres-employees/", views.show_dept_present_users, name="dept_pres_users"),
    path("HR-Dashboard/dept-late-employees/", views.show_dept_late_users, name="dept_late_users"),
    path("HR-Dashboard/dept-abs-employees/", views.show_dept_absent_users, name="dept_abs_users"),
    path("Admin-Dashboard/all-employees/", views.show_all_users, name="all_users"),
    path("Admin-Dashboard/all-pres-employees/", views.show_all_present_users, name="all_pres_users"),
    path("Admin-Dashboard/all-abs-employees/", views.show_all_absent_users, name="all_abs_users"),
    path("Admin-Dashboard/all-late-employees/", views.show_all_late_users, name="all_late_users"),



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