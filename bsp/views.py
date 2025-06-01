from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User
# Create your views here.
from bsp.forms import SignUpForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import User, DesignationList, DepartmentList, CheckLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError

from django.http import HttpResponseForbidden



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

    # context["time"] = timezone.now().time()

    return render(request, "bsp/MainPages/homepage.html", context)


@login_required(login_url="/accounts/login/")
def dept_hr_dashboard(request):
    context={
        "flag":0,
    }
    if user_is_dept_hr(request):
        context["flag"]=1

        if user_is_superuser(request):
            context["is_superuser"]=True

        return render(request, "bsp/MainPages/dash_hr.html", context)
    
    
    else:
        return HttpResponseForbidden("You do not have permission to view this resource.") 

@login_required(login_url="/accounts/login/")
def superuser_dashboard(request):
    context={
        "flag":0,
    }
    if user_is_superuser(request):
        context["flag"]=1

        if user_is_dept_hr(request):
            context["is_dept_hr"]=True

        return render(request, "bsp/MainPages/admin_dash.html", context)
    
    else:
        return HttpResponseForbidden("You do not have permission to view this resource.") 


@login_required(login_url="/accounts/login/")
def punching_home(request):
    context={}
    return render(request, "bsp/punches/phome.html", context)

@login_required(login_url="/accounts/login/")
def punch_in(request):
    uname=request.user.username
    user_obj = User.objects.get(username=uname)
    context={}

    to_allow = CheckLog.check_dup_in(username=user_obj)
    if to_allow:
        new_pin = CheckLog(username=user_obj, action_id=1, shift=CheckLog.match_time_to_shift(type="shift_start"))
        new_pin.save()

    else:
        context={"flag":1}
    return render(request, "bsp/punches/punchin.html", context)

@login_required(login_url="/accounts/login/")
def punch_out(request):
    uname=request.user.username
    user_obj = User.objects.get(username=uname)
    context={}

    to_allow = CheckLog.check_dup_out(username=user_obj)
    if to_allow:
        new_put = CheckLog(username=user_obj, action_id=2, shift=CheckLog.match_time_to_shift(type="shift_end"))
        new_put.save()

    else:
        context = {"flag":1}
    return render(request, "bsp/punches/punchout.html", context)


@login_required(login_url="/accounts/login/")
def punch_history(request):
    uname=request.user.username
    user_obj = User.objects.get(username=uname)
    matched_recs = CheckLog.objects.filter(username=user_obj)

    for i in matched_recs:
        if i.action_id==1:
            i.action_name="Punch-in"
        elif i.action_id==2:
            i.action_name="Punch-out"
            
    if matched_recs:
        context = {
            "punch_logs": matched_recs,
            "record_exists": 1,
    }
    return render(request, "bsp/punches/phist.html", context)






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


