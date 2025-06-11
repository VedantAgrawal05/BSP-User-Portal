from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User
# Create your views here.
from bsp.forms import SignUpForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import User, DesignationList, DepartmentList, CheckLog, Attendance, CommonClass, EmployeeDetails
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError

from django.http import HttpResponseForbidden
import random
import colorsys
import json


@login_required(login_url="/accounts/login/")
def homepage(request):
    if request.user.is_authenticated:
        
        uname=request.user.username
        user_obj = User.objects.get(username=uname)
        info = CommonClass.get_info(user_obj)
        context={
            "info":info,
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

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")


@login_required(login_url="/accounts/login/")
def dept_hr_dashboard(request):
    if request.user.is_authenticated:
        uname=request.user.username
        user_obj = User.objects.get(username=uname)
        info = CheckLog.get_todays_checkins_for_dept(user_obj)
        info["employee_details"] = EmployeeDetails.get_employee_details(user_obj)
        info["freq_late"]=CheckLog.get_frequent_late_arrivals(user_obj)
        info["excl_attend"], info["low_attend"] = Attendance.get_attendance_rates(user_obj)

        # raw_data = {
        #     'green': 50,
        #     'red': 30,
        #     'gray': 20
        # }

        # total = sum(raw_data.values())
        # current = 0
        # angles = {}

        # for key, value in raw_data.items():
        #     start = current
        #     end = current + (value / total * 360)
        #     angles[key + '_start'] = round(start, 2)
        #     angles[key + '_end'] = round(end, 2)
        #     current = end

        # context = {
        #     'green_start': angles['green_start'],
        #     'green_end': angles['green_end'],
        #     'red_start': angles['red_start'],
        #     'red_end': angles['red_end'],
        #     'gray_start': angles['gray_start'],
        #     'gray_end': angles['gray_end'],
        # }
        # return render(request, 'template.html', context)

        raw_data = {
            'green': info["present_count"],
            'yellow': info["late_count"],
            'gray': info["absent_count"],
        }

        total = sum(raw_data.values())
        angles = {}
        current_angle = 0

        for key, value in raw_data.items():
            angle = (value / total) * 360
            angles[f"{key}_start"] = round(current_angle, 2)
            current_angle += angle
            angles[f"{key}_end"] = round(current_angle, 2)

        # Pass the center color as a context variable if you want to make it dynamic
        context = {
            **angles,
            "info":info,
            "flag":0,
        }
            # 'center_color': '#2d3748'  # Change this to any hex or rgba
        

        if user_is_dept_hr(request):
            context["flag"]=1

            if user_is_superuser(request):
                context["is_superuser"]=True

            return render(request, "bsp/MainPages/dash_hr.html", context)
        
        
        else:
            return HttpResponseForbidden("You do not have permission to view this resource.") 

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")

@login_required(login_url="/accounts/login/")
def superuser_dashboard(request):
    if request.user.is_authenticated:
        uname=request.user.username
        user_obj = User.objects.get(username=uname)
        info={}
        info["employee_details"] = EmployeeDetails.get_employee_details(user_obj)
        context={
            "flag":0,
            
        }
        context["info"] = info
        # bar_data = [
        #     {'label': 'Production', 'height': 190},   # out of 200
        #     {'label': 'Maintenance', 'height': 176},
        #     {'label': 'Quality', 'height': 184},
        #     {'label': 'Admin', 'height': 196},
        #     {'label': 'Security', 'height': 170},
        #     {'label': 'Transport', 'height': 180},
        #     {'label': 'Finance', 'height': 160},
        #     {'label': 'IT', 'height': 150},
        #     {'label': 'Procurement', 'height': 172},
        #     {'label': 'Logistics', 'height': 168},
        # ]
        bar_data = CheckLog.get_todays_checkins_for_all_dept()
        lst1=[]
        lst2=[]
        for i in bar_data:
            lst1.append(i["label"])
            # lst2.append(i["height"])      """using height gives a percentage value, present_count gives count values"
            lst2.append(i["present_count"])

        barLabels = json.dumps(lst1)
        # barHeights = json.dumps(lst2)
        context['barLabels']=barLabels
        # context['barHeights']=b
        # arHeights

        # d1 = {'barLabels':lst1}
        # context['d1']=d1
        # context['barLabels']=lst1
        context['barHeights']=lst2
        context['bar_data']=bar_data
        all_emps_info=CommonClass.all_emps_info()
        all_emps_info["avg_attend"]=Attendance.get_average_attendance()
        # all_emps_info["tot_pres"]=CheckLog.get_total_present_today()
        # all_emps_info["tod_attend"]=
        context['all_emps_info']=all_emps_info

        dep_cnt = DepartmentList.objects.all().count() - 1
        context["piechartWeights"]=CommonClass.get_all_dept_emp_count()
        lst4 = CommonClass.generate_hex_colors(dep_cnt)
        bgColors = json.dumps(lst4)
        context["bgColors"]=bgColors
        
        a_months, attend_rates = CommonClass.get_attendance_trends()
        context["attendRates"] = attend_rates
        attend_months = json.dumps(a_months)
        context["attendMonths"] = attend_months

        if user_is_superuser(request):
            context["flag"]=1

            if user_is_dept_hr(request):
                context["is_dept_hr"]=True

            return render(request, "bsp/MainPages/admin_dash.html", context)
        
        else:
            return HttpResponseForbidden("You do not have permission to view this resource.") 

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")

@login_required(login_url="/accounts/login/")
def punch_in(request):
    if request.user.is_authenticated:
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

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")

@login_required(login_url="/accounts/login/")
def punch_out(request):
    if request.user.is_authenticated:
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

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")

@login_required(login_url="/accounts/login/")
def punch_history(request):
    if request.user.is_authenticated:
        uname=request.user.username
        user_obj = User.objects.get(username=uname)
        matched_recs = CheckLog.objects.filter(username=user_obj).order_by("-date", "-time")
        personal_details = CommonClass.get_info(user_obj)
        context={
            "record_exists":0,
            "info":personal_details,
        }
        # context[]
        for i in matched_recs:
            if i.action_id==1:
                i.action_name="Punch-in"
            elif i.action_id==2:
                i.action_name="Punch-out"
                
        if matched_recs:
            context = {
                "punch_logs": matched_recs,
                "record_exists": 1,
                "info":personal_details,
        }
        return render(request, "bsp/punches/phis_new.html", context)

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")


@login_required(login_url="/accounts/login/")
def attendance_history(request):
    if request.user.is_authenticated:
        uname=request.user.username
        user_obj = User.objects.get(username=uname)
        # matched_recs = CheckLog.objects.filter(username=user_obj)
        records = Attendance.get_formatted_values(uname)
        personal_details = CommonClass.get_info(user_obj)

        context={
            "record_exists":0,
            "info":personal_details,

        }
        if records:
            context = {
                "punch_logs": records,
                "record_exists": 1,
                "info":personal_details,
        }
        return render(request, "bsp/attendance/ahis_new.html", context)

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")



@login_required(login_url="/accounts/login/")
def show_dept_users(request):
    if request.user.is_authenticated:
        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users= CommonClass.get_dept_users(user_obj)
            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users,
            # "details":details,
            "flag":1,
            "info":personal_details,
                }
            
            return render(request, "bsp/users/duser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            

@login_required(login_url="/accounts/login/")
def show_dept_present_users(request):
    if request.user.is_authenticated:
        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_dept(user_obj)

            d1={}
            for usr in users_in_dept["present_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name
                usr.designation_name = usr.designation_id.designation_name
                usr.bsp_id = d1["bsp_id"]
                usr.phone = d1["phone"]
                usr.address = d1["corr_address"]
                usr.emer = d1["emergency_contact"]

            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users_in_dept["present_count"],
            # "details":details,
            "flag":1,
            "info":personal_details,
            "dept":user_obj.department_id.department_name,
            "type":"present",
                }
            
            return render(request, "bsp/users/wuser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_dept_absent_users(request):
    if request.user.is_authenticated:
        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_dept(user_obj)

            d1={}
            for usr in users_in_dept["absent_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name
                usr.designation_name = usr.designation_id.designation_name
                usr.bsp_id = d1["bsp_id"]
                usr.phone = d1["phone"]
                usr.address = d1["corr_address"]
                usr.emer = d1["emergency_contact"]

            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users_in_dept["absent_count"],
            # "details":details,
            "flag":1,
            "info":personal_details,
            "dept":user_obj.department_id.department_name,
            "type":"absent",
                }
            
            return render(request, "bsp/users/wuser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_dept_late_users(request):
    if request.user.is_authenticated:
        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_dept(user_obj)

            d1={}
            for usr in users_in_dept["late_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name
                usr.designation_name = usr.designation_id.designation_name
                usr.bsp_id = d1["bsp_id"]
                usr.phone = d1["phone"]
                usr.address = d1["corr_address"]
                usr.emer = d1["emergency_contact"]

            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users_in_dept["late_count"],
            # "details":details,
            "flag":1,
            "info":personal_details,
            "dept":user_obj.department_id.department_name,
            "type":"late",
                }
            
            return render(request, "bsp/users/wuser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_all_present_users(request):
    if request.user.is_authenticated:
        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_all_dept()

            d1={}
            for usr in users_in_dept["present_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name
                usr.designation_name = usr.designation_id.designation_name
                usr.bsp_id = d1["bsp_id"]
                usr.phone = d1["phone"]
                usr.address = d1["corr_address"]
                usr.emer = d1["emergency_contact"]

            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users_in_dept["present_count"],
            # "details":details,
            "flag":1,
            "info":personal_details,
            "dept":user_obj.department_id.department_name,
            "type":"present",
                }
            
            return render(request, "bsp/users/quser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_all_absent_users(request):
    if request.user.is_authenticated:
        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_all_dept()

            d1={}
            for usr in users_in_dept["absent_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name
                usr.designation_name = usr.designation_id.designation_name
                usr.bsp_id = d1["bsp_id"]
                usr.phone = d1["phone"]
                usr.address = d1["corr_address"]
                usr.emer = d1["emergency_contact"]

            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users_in_dept["absent_count"],
            # "details":details,
            "flag":1,
            "info":personal_details,
            "dept":user_obj.department_id.department_name,
            "type":"absent",
                }
            
            return render(request, "bsp/users/quser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_all_late_users(request):
    if request.user.is_authenticated:
        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_all_dept()

            d1={}
            for usr in users_in_dept["late_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name
                usr.designation_name = usr.designation_id.designation_name
                usr.bsp_id = d1["bsp_id"]
                usr.phone = d1["phone"]
                usr.address = d1["corr_address"]
                usr.emer = d1["emergency_contact"]

            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users_in_dept["late_count"],
            # "details":details,
            "flag":1,
            "info":personal_details,
            "dept":user_obj.department_id.department_name,
            "type":"late",
                }
            
            return render(request, "bsp/users/quser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            



        

@login_required(login_url="/accounts/login/")
def show_all_users(request):
    if request.user.is_authenticated:
        # uname=request.user.username
        if user_is_superuser(request):

        # user_obj = User.objects.get(username=uname)
        # return        if user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users= CommonClass.get_all_users()
            personal_details = CommonClass.get_info(user_obj)

            context={
            "users":users,
            # "details":details,
            "flag":1,
            "info":personal_details,
                }
            
            return render(request, "bsp/users/auser.html", context)


    else:
        return HttpResponseForbidden("You do not have permission to view this resource")



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
    if user_is_dept_hr(request):
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
    else:
        return HttpResponseForbidden("You do not have permission to view this resource")