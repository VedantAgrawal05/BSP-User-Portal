from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User
# Create your views here.
from bsp.forms import SignUpForm

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError

@login_required(login_url="/accounts/login/")
def homepage(request):
    context={
        "is_dept_hr": False,
        "is_read_only_superuser": False,
        "is_superuser": False,
    }
    if user_is_dept_hr(request):
        context["is_dept_hr"]=True
    
    if user_is_read_only_superuser(request):
        context["is_read_only_superuser"]=True

    if user_is_superuser(request):
        context["is_superuser"]=True

    return render(request, "bsp/MainPages/homepage.html", context)







@login_required(login_url="/accounts/login/")
def redirect_to_home(request):
    return redirect("bsp:home")


#for checking if user is dept hr
def user_is_dept_hr(request):
    uname=request.user.username
    user_obj = User.objects.get(username=uname)
    is_dept_hr = user_obj.is_dept_hr
    return is_dept_hr

#for checking if user is read-only superuser
def user_is_read_only_superuser(request):
    uname=request.user.username
    user_obj = User.objects.get(username=uname)
    is_read_only_superuser = user_obj.is_read_only_superuser
    return is_read_only_superuser

#for checking if user is superuser
def user_is_superuser(request):
    uname=request.user.username
    user_obj = User.objects.get(username=uname)
    is_superuser = user_obj.is_superuser
    is_staff = user_obj.is_staff
    res = is_staff and is_superuser
    return res








#login signup views stuff
# def signup(request):
#     if request.method=="POST":
#         # form = UserCreationForm(request.POST)
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             email = form.cleaned_data.get('email')
#             if User.objects.filter(email=email).exists():
#                 # raise ValidationError("Please choose unique email, this is already registered")            
#                 form = SignUpForm()
#                 return render(request, 'bsp/Accs/signup.html', {'form': form, 'flag':1})

#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect("bsp:home")
#     else:
#         # form = UserCreationForm()    
#         form = SignUpForm()

#     return render(request, 'bsp/Accs/signup.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            # Check email before saving
            if User.objects.filter(email=email).exists():
                return render(request, 'bsp/Accs/signup.html', {'form': form, 'flag': 1})

            # Save and log in
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("bsp:home")
    else:
        form = SignUpForm()

    return render(request, 'bsp/Accs/signup.html', {'form': form})


