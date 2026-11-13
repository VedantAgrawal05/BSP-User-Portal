from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bsp.forms import SignUpForm
from django.utils import timezone
from .models import User, DesignationList, DepartmentList, CheckLog, Attendance, CommonClass, EmployeeDetails, PayDetails
from bsp.utils.shifts import get_current_shift_info
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
import csv
import datetime
import random
import colorsys
import json

from django.utils.translation import gettext as _

from django.shortcuts import redirect
from django.utils import translation
# from django.utils.translation import LANGUAGE_SESSION_KEY

from django.conf import settings

# def set_language(request):
#     lang = request.GET.get('lang')
#     if lang in dict(settings.LANGUAGES):
#         request.session[LANGUAGE_SESSION_KEY] = lang
#     return redirect(request.META.get('HTTP_REFERER', '/'))


def set_language(request):
    lang = request.GET.get('lang')
    if lang in dict(settings.LANGUAGES):
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang  # ✅ This works, no need to import the constant
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="/accounts/login/")
def homepage(request):
    if request.user.is_authenticated:
        
        uname=request.user.username
        user_obj = User.objects.get(username=uname)
        info = CommonClass.get_info(user_obj)
        shift_info = get_current_shift_info(user_obj)
        context={
            "info":info,
            "shift_info": shift_info,
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
            time_str = new_pin.time.strftime('%I:%M %p') if hasattr(new_pin.time, 'strftime') else str(new_pin.time)
            messages.success(request, f"Successfully recorded Punch-in for Shift {new_pin.shift} at {time_str}!")
        else:
            context={"flag":1}
            messages.warning(request, "Punch-in already recorded recently for today.")
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
            time_str = new_put.time.strftime('%I:%M %p') if hasattr(new_put.time, 'strftime') else str(new_put.time)
            messages.success(request, f"Successfully recorded Punch-out for Shift {new_put.shift} at {time_str}!")
        else:
            context = {"flag":1}
            messages.warning(request, "Punch-out already recorded recently for today.")
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
        if user_is_superuser(request) or user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_dept(user_obj)

            d1={}
            for usr in users_in_dept["present_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name if usr.department_id else "Not Assigned"
                usr.designation_name = usr.designation_id.designation_name if usr.designation_id else "Not Assigned"
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
                "dept":user_obj.department_id.department_name if user_obj.department_id else "Not Assigned",
                "type":"present",
            }
            
            return render(request, "bsp/users/wuser.html", context)

        else:
            return HttpResponseForbidden("You do not have permission to view this resource")
    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_dept_absent_users(request):
    if request.user.is_authenticated:
        if user_is_superuser(request) or user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_dept(user_obj)

            d1={}
            for usr in users_in_dept["absent_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name if usr.department_id else "Not Assigned"
                usr.designation_name = usr.designation_id.designation_name if usr.designation_id else "Not Assigned"
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
                "dept":user_obj.department_id.department_name if user_obj.department_id else "Not Assigned",
                "type":"absent",
            }
            
            return render(request, "bsp/users/wuser.html", context)

        else:
            return HttpResponseForbidden("You do not have permission to view this resource")
    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_dept_late_users(request):
    if request.user.is_authenticated:
        if user_is_superuser(request) or user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_dept(user_obj)

            d1={}
            for usr in users_in_dept["late_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name if usr.department_id else "Not Assigned"
                usr.designation_name = usr.designation_id.designation_name if usr.designation_id else "Not Assigned"
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
                "dept":user_obj.department_id.department_name if user_obj.department_id else "Not Assigned",
                "type":"late",
            }
            
            return render(request, "bsp/users/wuser.html", context)

        else:
            return HttpResponseForbidden("You do not have permission to view this resource")
    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_all_present_users(request):
    if request.user.is_authenticated:
        if user_is_superuser(request) or user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_all_dept()

            d1={}
            for usr in users_in_dept["present_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name if usr.department_id else "Not Assigned"
                usr.designation_name = usr.designation_id.designation_name if usr.designation_id else "Not Assigned"
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
                "dept":user_obj.department_id.department_name if user_obj.department_id else "Not Assigned",
                "type":"present",
            }
            
            return render(request, "bsp/users/quser.html", context)
        else:
            return HttpResponseForbidden("You do not have permission to view this resource")

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_all_absent_users(request):
    if request.user.is_authenticated:
        if user_is_superuser(request) or user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_all_dept()

            d1={}
            for usr in users_in_dept["absent_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name if usr.department_id else "Not Assigned"
                usr.designation_name = usr.designation_id.designation_name if usr.designation_id else "Not Assigned"
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
                "dept":user_obj.department_id.department_name if user_obj.department_id else "Not Assigned",
                "type":"absent",
            }
            
            return render(request, "bsp/users/quser.html", context)
        else:
            return HttpResponseForbidden("You do not have permission to view this resource")

    else:
        return HttpResponseForbidden("You do not have permission to view this resource")
            


@login_required(login_url="/accounts/login/")
def show_all_late_users(request):
    if request.user.is_authenticated:
        if user_is_superuser(request) or user_is_dept_hr(request):
            uname=request.user.username
            user_obj = User.objects.get(username=uname)
            users_in_dept= CommonClass.get_todays_users_for_all_dept()

            d1={}
            for usr in users_in_dept["late_count"]:
                d1 = EmployeeDetails.get_employee_details(usr)
                usr.department_name = usr.department_id.department_name if usr.department_id else "Not Assigned"
                usr.designation_name = usr.designation_id.designation_name if usr.designation_id else "Not Assigned"
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
                "dept":user_obj.department_id.department_name if user_obj.department_id else "Not Assigned",
                "type":"late",
            }
            
            return render(request, "bsp/users/quser.html", context)
        else:
            return HttpResponseForbidden("You do not have permission to view this resource")

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
    if user_is_superuser(request) or user_is_dept_hr(request):
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')

                # Check email before saving
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"An employee with email '{email}' already exists.")
                    return render(request, 'bsp/Accs/signup.html', {'form': form, 'flag': 1})

                # Save user with selected department and designation
                user = form.save(commit=False)
                dept_val = form.cleaned_data.get('department')
                desg_val = form.cleaned_data.get('designation')
                if dept_val:
                    try:
                        user.department_id = DepartmentList.objects.get(department_id=dept_val)
                    except DepartmentList.DoesNotExist:
                        pass
                if desg_val:
                    try:
                        user.designation_id = DesignationList.objects.get(designation_id=desg_val)
                    except DesignationList.DoesNotExist:
                        pass
                user.save()

                # Also create EmployeeDetails so user has a complete profile
                EmployeeDetails.objects.get_or_create(
                    username=user,
                    defaults={
                        'res_address': 'SAIL Township, Bhilai',
                        'corr_address': 'SAIL Township, Bhilai',
                        'phone_number': 9999999999,
                        'emergency_contact_name': 'Emergency Contact',
                        'emergency_contact_number': 9999999999,
                    }
                )

                messages.success(request, f"User account '{user.username}' ({user.first_name} {user.last_name}) created successfully!")

                if user_is_superuser(request):
                    return redirect("bsp:superuser_dash")
                elif user_is_dept_hr(request):
                    return redirect("bsp:hr_dash")
                else:
                    return redirect("bsp:home")
        else:
            form = SignUpForm()

        return render(request, 'bsp/Accs/signup.html', {'form': form})
    else:
        return HttpResponseForbidden("You do not have permission to view this resource")


@login_required(login_url="/accounts/login/")
def export_employees_csv(request):
    """
    Exports all employee records as a CSV spreadsheet.
    """
    if not (user_is_superuser(request) or user_is_dept_hr(request)):
        return HttpResponseForbidden("Permission denied.")

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="SAIL_BSP_Employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['BSP ID', 'Username', 'First Name', 'Last Name', 'Department', 'Designation', 'Email', 'Phone', 'Date Joined', 'Residential Address'])

    users = CommonClass.get_all_users()
    for u in users:
        writer.writerow([
            getattr(u, 'bsp_id', f"BSP{u.id:05d}"),
            u.username,
            u.first_name,
            u.last_name,
            u.department_id.department_name if u.department_id else 'Not Assigned',
            u.designation_id.designation_name if u.designation_id else 'Not Assigned',
            u.email,
            getattr(u, 'phone', 'N/A'),
            u.date_joined,
            getattr(u, 'address', 'N/A'),
        ])
    return response


@login_required(login_url="/accounts/login/")
def export_attendance_csv(request):
    """
    Exports today's attendance roster across all departments as a CSV spreadsheet.
    """
    if not (user_is_superuser(request) or user_is_dept_hr(request)):
        return HttpResponseForbidden("Permission denied.")

    today_str = datetime.date.today().strftime('%Y-%m-%d')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="SAIL_BSP_Attendance_{today_str}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'BSP ID', 'Username', 'Full Name', 'Department', 'Designation', 'Status'])

    todays_data = CommonClass.get_todays_users_for_all_dept()
    for u in todays_data.get('present_count', []):
        d1 = EmployeeDetails.get_employee_details(u)
        writer.writerow([
            today_str,
            d1.get('bsp_id', f"BSP{u.id:05d}"),
            u.username,
            d1.get('full_name', u.username),
            u.department_id.department_name if u.department_id else 'Not Assigned',
            u.designation_id.designation_name if u.designation_id else 'Not Assigned',
            'Present',
        ])
    for u in todays_data.get('absent_count', []):
        d1 = EmployeeDetails.get_employee_details(u)
        writer.writerow([
            today_str,
            d1.get('bsp_id', f"BSP{u.id:05d}"),
            u.username,
            d1.get('full_name', u.username),
            u.department_id.department_name if u.department_id else 'Not Assigned',
            u.designation_id.designation_name if u.designation_id else 'Not Assigned',
            'Absent',
        ])
    return response


@login_required(login_url="/accounts/login/")
def view_payslip(request):
    """
    Renders an official, printable SAIL Bhilai Steel Plant monthly payslip.
    """
    user_obj = request.user
    emp_details = EmployeeDetails.get_employee_details(user_obj)
    sal_details = PayDetails.get_sal_details(user_obj)

    today = datetime.date.today()
    month_str = today.strftime("%B %Y")

    context = {
        "user": user_obj,
        "emp": emp_details,
        "sal": sal_details,
        "month_str": month_str,
        "today": today,
    }
    return render(request, "bsp/payslip.html", context)
