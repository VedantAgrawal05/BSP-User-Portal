from datetime import date
from django.db import models

from django.contrib.auth.models import AbstractUser#, User
import datetime, calendar
import colorsys, random
from dateutil.relativedelta import relativedelta


# Create your models here.
class DepartmentList(models.Model):
    department_id = models.PositiveSmallIntegerField('Department ID', primary_key=True)
    department_name = models.CharField("Department Name", max_length=200)

class DesignationList(models.Model):
    designation_id = models.PositiveSmallIntegerField('Designation ID', primary_key=True)
    designation_name = models.CharField("Designation Name", max_length=200)

class User(AbstractUser):
    #fields
    '''
    designation 
    dept

    is_dept_hr
    is_read_only_superuser
    '''
    """
    #currently using only one table, may split into different in future
    department = models.CharField(max_length=200)
    department_id = models.PositiveSmallIntegerField(blank=True, null=True)

    designation = models.CharField(max_length=200)
    designation_id = models.PositiveSmallIntegerField(blank=True, null=True)
    """
    #currently using only one table, may split into different in future
    # department = models.CharField(max_length=200)
    department_id = models.ForeignKey(DepartmentList, on_delete=models.SET_NULL, null=True, default=1)

    # designation = models.CharField(max_length=200)
    designation_id = models.ForeignKey(DesignationList, on_delete=models.SET_NULL, null=True, default=3)
    
    #overriding date_joined
    date_joined = models.DateField(default=datetime.datetime.today().date())
    birthday = models.DateField(blank=True, null=True)

    email = models.EmailField(unique=True)

    #power related roles
    is_dept_hr = models.BooleanField(default=0)
    is_read_only_superuser = models.BooleanField(default=0)

    class Meta:
        db_table='auth_user'

    def __str__(self):
        return self.username
    
    def get_user_age(self):
        born = self.birthday
        today = datetime.datetime.today()

        try:
            bday = born.replace(year = today.year)

        #handling edge case for 29th feb
        except ValueError:
            bday = born.replace(year = today.year, month = born.month+1, day=1)

        if bday>today:
            return today.year - born.year - 1

        else:
            return today.year - born.year
        
class CheckLog(models.Model):
    #action id 1 is used to represent punch in, action id 2 represents punch out
    action_id=models.PositiveSmallIntegerField("Action Id")

    username=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    shift=models.CharField(max_length=1, null=True, default="D")

    def __str__(self):
        str1= f"{self.username} "
        if self.action_id==1:
            str1+="Punch-in"

        elif self.action_id==2:
            str1+="Punch-out"

        return str1
    
    def check_dup_in(username):
        curr_date = CheckLog.get_current_date()
        recs = CheckLog.objects.filter(username= username, date=curr_date, action_id=1).order_by('-time')  

        curr_time = CheckLog.get_current()
        # diff = curr_time - datetime.timedelta(minutes=30)
        diff = (curr_time - datetime.timedelta(minutes=10)).time()

        # for i in recs:
        #     if diff < i.time:
        #         return False
        #     elif diff >  i.time:
        #         return True
        #     else:
        #         return False

        try:
            to_check = recs[0]
        except IndexError:
            return True
        
        if diff < to_check.time:
            return False
        elif diff >  to_check.time:
            return True
        else:
            return False

    def check_dup_out(username):
        curr_date = CheckLog.get_current_date()
        recs = CheckLog.objects.filter(username= username, date=curr_date, action_id=2).order_by('-time')  

        curr_time = CheckLog.get_current()
        # diff = curr_time - datetime.timedelta(minutes=30)
        diff = (curr_time - datetime.timedelta(minutes=10)).time()


        # for i in recs:
        #     if diff < i.time:
        #         return False
        #     elif diff >  i.time:
        #         return True
        #     else:
        #         return False
        

        try:
            to_check = recs[0]
        except IndexError:
            return True
        
        if diff < to_check.time:
            return False
        elif diff >  to_check.time:
            return True
        else:
            return False
    

    def get_current():
        return datetime.datetime.now()
        
    def get_current_date():
        ab = CheckLog.get_current()
        return ab.date()

    def get_current_time():
        ab = CheckLog.get_current()
        return ab.time()
    

    def match_time_to_shift(type):
        # Current time
        now = CheckLog.get_current_time()

        # Define time points (you can add more)
        time_points_start = {
            datetime.time(6, 0): "A",
            datetime.time(9, 0): "G",
            datetime.time(14, 0): "B",
            datetime.time(22, 0): "C",
        }
        
        time_points_end = {
            datetime.time(14, 0): "A",
            datetime.time(17, 0): "G",
            datetime.time(22, 0): "B",
            datetime.time(6, 0): "C",
        }

        # Tolerance in minutes
        tolerance = datetime.timedelta(minutes=30)

        # Convert current time to datetime for comparison
        now_dt = datetime.datetime.combine(datetime.datetime.today(), now)

        if type=="start" or type==0 or type=="shift_start":
            for t_point, value in time_points_start.items():
                point_dt = datetime.datetime.combine(datetime.datetime.today(), t_point)
                if abs(now_dt - point_dt) <= tolerance:
                    return value

        elif type=="end" or type==1 or type=="shift_end":
            for t_point, value in time_points_end.items():
                point_dt = datetime.datetime.combine(datetime.datetime.today(), t_point)
                if abs(now_dt - point_dt) <= tolerance:
                    return value

        # Default unique value if no match
        return "D"

    def get_recent_activities(uobj):
        recs = CheckLog.objects.filter(username=uobj).order_by("-date","-time")[:4]
        lst=[]
        for iter in recs:
            lst2=[]

            if iter.action_id==1:
                action="Punch-in"

            elif iter.action_id==2:
                action="Punch-out"
            lst2.append(action)

            tm = iter.time
            time = tm.strftime("%I:%M %p").lstrip("0")
            lst2.append(time)

            dt = iter.date
            date = CheckLog.date_to_str(dt)
            lst2.append(date)
            lst.append(lst2)
            lst2=[]

        return lst

    def date_to_str(dt):    
        today = CheckLog.get_current_date()
        delta = today - dt
    
        days = delta.days

        if days < 0:
            return "in the future"
        elif days == 0:
            return "today"
        elif days == 1:
            return "yesterday"
        elif days < 7:
            return f"{days} days ago"
        elif days < 14:
            return "1 week ago"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} weeks ago"
        elif days < 60:
            return "1 month ago"
        elif days < 365:
            months = days // 30
            return f"{months} months ago"
        elif days < 730:
            return "1 year ago"
        else:
            years = days // 365
            return f"{years} years ago"
        
    def get_todays_checkins_for_dept(uobj):
        # dept = DepartmentList.objects.get()
        dept = uobj.department_id
        # dobj = DesignationList.objects.get(designation_id=desgn)
        # dobj = DepartmentList.objects.get(department_id=dept)
        # sal_
        info={}
        # rec = CheckLog.objects.get(designation_id=desgn)
        users_in_dept = User.objects.filter(department_id=dept)
        total_users = len(users_in_dept)

        tod = CheckLog.get_current_date()

        todays_checkins = CheckLog.objects.filter(action_id=1, date=tod)
        # print(CheckLog.objects.filter(action_id=1, date=tod).query)

        present_count =0
        absent_count =0
        late_count=0

        # for i in users_in_dept:
        #     for j in todays_checkins:
        #         if j.username==i:
        #             ch_in = j.time
        #             sh = j.shift
        #             if CheckLog.check_if_user_late(ch_in, sh):
        #                 late_count+=1
        #                 present_count+=1
        #                 break

        #             else:
        #                 present_count+=1
        #             # present_users.append(i)
                    
        #         else:
        #             absent_count+=1

        found = False
        for i in users_in_dept:
            for j in todays_checkins:
                if j.username==i:
                    ch_in = j.time
                    sh = j.shift
                    if CheckLog.check_if_user_late(ch_in, sh):
                        late_count+=1
                    present_count+=1
                    found = True
                    break

                    # else:
                        # present_count+=1
                    # present_users.append(i)

            if not found:
                    absent_count+=1
                    found=False

        try:
            chk = (present_count / (present_count + absent_count ))*100
            attendance_rate= round(chk, 2)
        except ZeroDivisionError:
            attendance_rate=0

        # for k in present_users:
        info["present_count"]=present_count
        info["absent_count"]=absent_count
        info["late_count"]=late_count
        info["total_employees"]=total_users
        info["rate"]=attendance_rate

        return info

        
    def get_frequent_late_arrivals(uobj):
        # dept = DepartmentList.objects.get()
        dept = uobj.department_id
        # dobj = DesignationList.objects.get(designation_id=desgn)
        # dobj = DepartmentList.objects.get(department_id=dept)
        # sal_
        freq_late_count=0
        late_count = 0
        # rec = CheckLog.objects.get(designation_id=desgn)
        users_in_dept = User.objects.filter(department_id=dept)

        for usr in users_in_dept:
            checks = CheckLog.objects.filter(action_id=1, username=usr).order_by("-date")[:30]
            for chk in checks:
                ch_in = chk.time
                sh = chk.shift
                if CheckLog.check_if_user_late(ch_in, sh):
                    late_count+=1

            if late_count/30 > 0.35: #more than 355 arrival was late
                freq_late_count+=1
            
            late_count=0

        # found = False
        # for i in users_in_dept:
        #     for j in todays_checkins:
        #         if j.username==i:
        #             ch_in = j.time
        #             sh = j.shift
        #             if CheckLog.check_if_user_late(ch_in, sh):
        #                 late_count+=1
        #             present_count+=1
        #             found = True
        #             break

        #             # else:
        #                 # present_count+=1
        #             # present_users.append(i)

        #     if not found:
        #             absent_count+=1
        #             found=False

        # try:
        #     chk = (present_count / (present_count + absent_count ))*100
        #     attendance_rate= round(chk, 2)
        # except ZeroDivisionError:
        #     attendance_rate=0

        # for k in present_users:
        # info["present_count"]=present_count
        # info["absent_count"]=absent_count
        # info["late_count"]=late_count
        # info["total_employees"]=total_users
        # info["rate"]=attendance_rate


        return freq_late_count


    def get_todays_checkins_for_all_dept():
        # dept = DepartmentList.objects.get()
        # dept = uobj.department_id
        # dobj = DesignationList.objects.get(designation_id=desgn)
        # dobj = DepartmentList.objects.get(department_id=dept)
        # sal_
        info={}
        # rec = CheckLog.objects.get(designation_id=desgn)
        all_users = User.objects.all()
        total_users = len(all_users)
        all_depts = DepartmentList.objects.all()
        tod = CheckLog.get_current_date()
        todays_checkins = CheckLog.objects.filter(action_id=1, date=tod)
        # print(CheckLog.objects.filter(action_id=1, date=tod).query)

        dep_info = {}
        # absent_count = [] 
        d1 = {}

        for i in all_depts:
            if i.department_id==0:
                continue
            d1 = {"label":i.department_name, "height":0, "present_count":0, "absent_count":0}
            dep_info[i.department_name] = d1
            d1={}
        # late_count= 0
        found = False

    #for i in all depts
        # for dep in all_depts:
        for usr in all_users:
            for chkin in todays_checkins:
                    #dept ==i
                if chkin.username==usr:
                    # ch_in = chkin.time
                    # sh = chkin.shift
                    # if CheckLog.check_if_user_late(ch_in, sh):
                    #     late_count+=1
            
                    dep_info[usr.department_id.department_name]["present_count"]+=1
                    found = True
                    break

                    # else:
                        # present_count+=1
                    # present_users.append(i)

            if not found:

                    dep_info[usr.department_id.department_name]["absent_count"]+=1
                    found=False

        for iter in dep_info:
            pc= dep_info[iter]["present_count"]
            ac= dep_info[iter]["absent_count"]
            try:
                chk = (pc / (pc + ac ))*200
                hgt= round(chk, 1)
            except ZeroDivisionError:
                hgt = 0
            dep_info[iter]["height"] = hgt
            

        # # for k in present_users:
        # info["present_count"]=present_count
        # info["absent_count"]=absent_count
        # # info["late_count"]=late_count
        # info["total_employees"]=total_users
        # info["rate"]=attendance_rate
        lst1 = [dep_info[x] for x in dep_info] 

        for r in lst1:
            if r["label"]=="Human Resources":
                r["label"]="HR"
            elif r["label"]=="Research and Development":
                r["label"]="R & D"
            elif r["label"]=="Customer Support":
                r["label"]="Support"
            elif r["label"]=="IT Services":
                r["label"]="IT"
            
        return lst1



    def get_total_present_today():
        # dept = DepartmentList.objects.get()
        # dept = uobj.department_id
        # dobj = DesignationList.objects.get(designation_id=desgn)
        # dobj = DepartmentList.objects.get(department_id=dept)
        # sal_
        # info={}
        # rec = CheckLog.objects.get(designation_id=desgn)
        # all_users = User.objects.all()
        # total_users = len(all_users)
        # all_depts = DepartmentList.objects.all()
        tod = CheckLog.get_current_date()
        todays_checkins = CheckLog.objects.filter(action_id=1, date=tod).count()
        return todays_checkins
        # print(CheckLog.objects.filter(action_id=1, date=tod).query)

    #     # dep_info = {}
    #     # absent_count = [] 
    #     # d1 = {}

    #     # for i in all_depts:
    #         # if i.department_id==0:
    #             # continue
    #         # d1 = {"label":i.department_name, "height":0, "present_count":0, "absent_count":0}
    #         # dep_info[i.department_name] = d1
    #         # d1={}
    #     # late_count= 0
    #     # found = False

    # #for i in all depts
    #     # for dep in all_depts:
    #     for usr in all_users:
    #         for chkin in todays_checkins:
    #                 #dept ==i
    #             if chkin.username==usr:
    #                 # ch_in = chkin.time
    #                 # sh = chkin.shift
    #                 # if CheckLog.check_if_user_late(ch_in, sh):
    #                 #     late_count+=1
            
    #                 dep_info[usr.department_id.department_name]["present_count"]+=1
    #                 found = True
    #                 break

    #                 # else:
    #                     # present_count+=1
    #                 # present_users.append(i)

    #         if not found:

    #                 dep_info[usr.department_id.department_name]["absent_count"]+=1
    #                 found=False

    #     for iter in dep_info:
    #         pc= dep_info[iter]["present_count"]
    #         ac= dep_info[iter]["absent_count"]
    #         try:
    #             chk = (pc / (pc + ac ))*200
    #             hgt= round(chk, 1)
    #         except ZeroDivisionError:
    #             hgt = 0
    #         dep_info[iter]["height"] = hgt
            

    #     # # for k in present_users:
    #     # info["present_count"]=present_count
    #     # info["absent_count"]=absent_count
    #     # # info["late_count"]=late_count
    #     # info["total_employees"]=total_users
    #     # info["rate"]=attendance_rate
    #     lst1 = [dep_info[x] for x in dep_info] 

    #     for r in lst1:
    #         if r["label"]=="Human Resources":
    #             r["label"]="HR"
    #         elif r["label"]=="Research and Development":
    #             r["label"]="R & D"
    #         elif r["label"]=="Customer Support":
    #             r["label"]="Support"
    #         elif r["label"]=="IT Services":
    #             r["label"]="IT"
            
    #     return lst1


    def check_if_user_late(time, shift):
        dt = datetime.date(2000,1,5)
        time_dt = datetime.datetime.combine(dt, time)

        if shift=="A":
            shift_time = datetime.time(6,0)

        elif shift=="G":
            shift_time = datetime.time(9,0)

        elif shift=="B":
            shift_time = datetime.time(14,0)

        elif shift=="C":
            shift_time = datetime.time(22,0)

        elif shift=="D":
            return 1
                
        comp_dt = datetime.datetime.combine(dt, shift_time)
        zero_time = datetime.timedelta(minutes=0)
        grace_time = datetime.timedelta(minutes=10)
        if (comp_dt - time_dt)>zero_time:
            return 0                

        else:
            if (time_dt - comp_dt)>grace_time:
                return 1
            
            else: 
                return 0
            

#similar to checklog, 1 is used to represent present. no entry or 0 signifies absent. 2 will represent user was there but did not work enough for full attendance
class Attendance(models.Model):
    username=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date=models.DateField(default=datetime.date.today())
    was_present=models.PositiveSmallIntegerField("Present or Absent", default=0)
    shift=models.CharField(max_length=1, null=True, default="D")
    hours_worked=models.DecimalField("Hours worked", max_digits=4, decimal_places=2)


    def __str__(self):
        return f"{self.username} {self.was_present}"
    

    def get_formatted_values(uname):
        user_obj = User.objects.get(username=uname)
        Attendance.absent_days_populator(user_obj)

        user_recs = Attendance.objects.filter(username=user_obj).order_by("-date")
        if user_recs:
            for iter in user_recs:
                #for shift names
                if iter.shift=="A":
                    iter.shift="Morning Shift"
                elif iter.shift=="B":
                    iter.shift="Day Shift"
                elif iter.shift=="C":
                    iter.shift="Night Shift"
                elif iter.shift=="G":
                    iter.shift="General Shift"
                elif iter.shift=="D" and iter.was_present==0:
                    iter.shift="None"
                elif iter.shift=="D":
                    iter.shift="Partial Shift"

                #for was_present column
                if iter.was_present == 0:
                    iter.was_present="Absent"
                    iter.attend_class="status-absent"
                elif iter.was_present == 1:
                    iter.was_present="Present"
                    iter.attend_class="status-present"
                elif iter.was_present == 2:
                    iter.was_present="Partial Day"
                    iter.attend_class="status-partial"
        else:
            user_recs=[]
            
        return user_recs
                

    def absent_days_populator(uobj):
        user_obj = uobj
        # user_obj = User.objects.get(username=uname)
        logs = Attendance.objects.filter(username=user_obj,was_present=0).order_by("-date")
        if logs:
            start=logs[0].date + datetime.timedelta(days=1)

        else:
            start = date(2025, 5, 25)  # Replace with the desired start date

        # def get_date_list(start_date):
        today = Attendance.get_current().date()
        delta = today - start
        dates_list = [start + datetime.timedelta(days=i) for i in range(delta.days)]
        # return dates_list

        # Example usage
        # date_list = get_date_list(start)

        # # Print the result
        # for d in date_list:
        #     print(d)

        for iter in dates_list:
            if iter.weekday()!=6:  #not a sunday
                rec=Attendance.objects.filter(username=user_obj, date=iter)

                if not rec:
                    # for 
                    # i in rec:
                    new_abs = Attendance(username=user_obj, date=iter,was_present=0, hours_worked=0)
                    new_abs.save()

    # def record_updater(self, instance):
    #     print("yoooo")
    def get_current():
        return datetime.datetime.now()

    def get_dates():
        now = Attendance.get_current()
        # info = {}
        today = now.date()
        year = now.year
        month = now.month
        num_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
        fin=[]
        for d in days:
            if d<=today:
                if d.weekday()!=6:
                    fin.append(d)
            else:
                break
        return fin

    def get_current_week_dates():
        today = date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday
        return [start_of_week + datetime.timedelta(days=i) for i in range((today - start_of_week).days + 1)]

    def get_attendance_percentage(uobj):
        user_obj = uobj
        Attendance.absent_days_populator(uobj)
        # user_obj = User.objects.get(username=uname)
        absent_count = 0
        present_count = 0
        logs = Attendance.objects.filter(username=user_obj).order_by("-date")[:30]
        for iter in logs:
            if iter.was_present==1:
                present_count += 1
            else:
                absent_count += 1

       
        chk = (present_count / (present_count + absent_count))*100
        rate= round(chk, 2)

        return rate
    
    def get_attendance_rates(hr_uobj):
        dept = hr_uobj.department_id
        users_in_dept = User.objects.filter(department_id=dept)
        users_attendances = []
        for usr in users_in_dept:
            atnd = Attendance.get_attendance_percentage(usr)
            users_attendances.append(atnd)

        high_count = 0
        low_count = 0

        for i in users_attendances:
            if i>=95:
                high_count+=1
            elif i<85:
                low_count+=1

        # attendance_rate = {
        #     "high":high_count,
        #     "low":low_count,
        # }

        return high_count, low_count
        
    def get_average_attendance():
        all_users = User.objects.all()
        atends = []
        for usr in all_users:
            atends.append(Attendance.get_attendance_percentage(usr))

        sum2=0
        for i in atends:
            sum2+=i

        cnt = len(atends)

        average_atend = sum2/cnt
        ret = round(average_atend, 2)
        return f"{ret}%"



class PayDetails(models.Model):
    designation_id = models.ForeignKey(DesignationList, on_delete=models.SET_NULL, null=True)
    basic_salary= models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.designation_id} {self.net_salary}"
    
    def get_sal_details(uobj):
        desgn = uobj.designation_id
        # dobj = DesignationList.objects.get(designation_id=desgn)
        sal_rec = PayDetails.objects.get(designation_id=desgn)
        basic_salary = CommonClass.format_indian_currency(sal_rec.basic_salary)
        allowances =  CommonClass.format_indian_currency(sal_rec.allowances)
        deductions=  CommonClass.format_indian_currency(sal_rec.deductions)
        net_salary =  CommonClass.format_indian_currency(sal_rec.net_salary)
        sal_details = {
            "basic_salary":basic_salary,
            "allowances":allowances,
            "deductions":deductions,
            "net_salary":net_salary,
        }
        return sal_details

class EmployeeDetails(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    res_address = models.CharField(max_length=300)
    corr_address = models.CharField(max_length=300)
    phone_number = models.BigIntegerField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.BigIntegerField()


    def format_code(number):
        """
    Format the number as 'BSP00000' with zero padding to make it 5 digits.
    """
        return f"BSP{number:05d}"

    def get_employee_details(uobj):
        rec = EmployeeDetails.objects.get(username=uobj)
        uid= uobj.id
        desgn_id=uobj.designation_id
        dept_id=uobj.department_id
        bsp_id = EmployeeDetails.format_code(uid)
        # dept_rec = DepartmentList.objects.get(designation_id=desgn_id)
        
        emp_details= {
            "bsp_id":bsp_id,
            "full_name":f"{uobj.first_name} {uobj.last_name}",
            "department": dept_id.department_name,
            "designation":desgn_id.designation_name,
            "date_joined":uobj.date_joined,
            "email":uobj.email,
            "phone":rec.phone_number,
            "res_address":rec.res_address,
            "corr_address":rec.corr_address,
            "emergency_contact":f'{rec.emergency_contact_name} - {rec.emergency_contact_number}',

        }
        return emp_details


class CommonClass(): 
    def get_info(uobj):
        Attendance.absent_days_populator(uobj)
        # recs = Attendance.objects.filter(username=uobj).sort_by('-date')[:35]
        month_dates = Attendance.get_dates()
        present_count = 0
        absent_count = 0
        total_hours = 0

        for iter in month_dates:
            try:
                rec = Attendance.objects.filter(username=uobj, date=iter)[0]
                total_hours += rec.hours_worked
            except IndexError:
                pass
            
            if rec.was_present==1:
                present_count+=1
            elif rec.was_present==0:
                absent_count+=1

        try:
            chk = (present_count / (present_count + absent_count))*100
            rate= round(chk, 2)

        except ZeroDivisionError:
            rate=0

        info = {
            "present_count":present_count,
            "absent_count":absent_count,
            "total_hours":total_hours,
            "rate":rate,
        }

        #weekly graph
        weekly_hours = []
        dates= Attendance.get_current_week_dates()
        for dt in dates:
            try:
                rec=Attendance.objects.filter(username=uobj, date=dt)[0]
                perc = (rec.hours_worked/8)*100
            except IndexError:
                perc=0
            as_pe = f"{perc}%"
            weekly_hours.append(as_pe)

        info["weekly_hours"]=weekly_hours

        recent_activities = CheckLog.get_recent_activities(uobj)

        info["recent_activities"]=recent_activities
        info["len_of_recents"]=len(recent_activities)

        salay_details = PayDetails.get_sal_details(uobj)
        info["salary_details"]=salay_details

        employee_details = EmployeeDetails.get_employee_details(uobj)
        info["employee_details"]=employee_details


        return info
    
    def format_indian_currency(number):
        formatted = CommonClass.indian_currency_commas(number)
        str1 = f"₹{formatted}"
        return str1
    
    def indian_currency_commas(number):    
        number = int(round(number))  # Remove decimals
        num_str = str(number)
        if len(num_str) <= 3:
            return num_str
        else:
            # Split last 3 digits and the rest
            last_three = num_str[-3:]
            remaining = num_str[:-3]
            # Add commas after every 2 digits in the remaining part
            parts = []
            while len(remaining) > 2:
                parts.insert(0, remaining[-2:])
                remaining = remaining[:-2]
            if remaining:
                parts.insert(0, remaining)
            return ','.join(parts) + ',' + last_three

    def all_emps_info():
        emp_info= {}
        all_emps = User.objects.all()
        emp_info["num_emps"] = User.objects.count()

        all_depts = DepartmentList.objects.all()
        emp_info["num_depts"] = DepartmentList.objects.count() - 1

        emp_info["tot_pres"]=CheckLog.get_total_present_today()

        emp_info["tod_attend"]= f"{round((emp_info["tot_pres"]/emp_info["num_emps"])*100,2)}%"
        return emp_info

    def get_all_dept_emp_count():
        depts = DepartmentList.objects.all()
        
        emp_counts = []
        for i in depts:
            if i.department_id!=0:
                emps = User.objects.filter(department_id=i).count()
                emp_counts.append(emps)

        return emp_counts
    

    def get_attendance_trends():
        past_months = CommonClass.get_last_6_months()
        attend_rates = {}

        c_mon = CommonClass.get_current().month
        curr_mon = calendar.month_abbr[c_mon]
        curr_dt = CommonClass.get_current().day

        for mon in past_months:
            ky=calendar.month_abbr[mon[0]]
            
            if mon[0]!=c_mon:
                days = CommonClass.count_working_days(mon[0],mon[1])
            elif mon[0]==c_mon:
                days = CommonClass.count_working_days_current_month()

            attend_rates[ky]=[0,days]
                # attend_rates[ky]=[0,days]

        ar_sum = 0
        users = User.objects.all()
        user_count = users.count()
        for usr in users:
            Attendance.absent_days_populator(usr)

        recs = Attendance.objects.all()

        for iter in recs:
            dt = iter.date
            mn = dt.month
            yr= dt.year
            tup=(mn,yr)

            if tup in past_months and iter.was_present==1:
                attend_rates[calendar.month_abbr[mn]][0]+=1
        
        """should be actually working days (month-sundays) and multiplied by total employees"""
        for i in attend_rates:
            if i!=curr_mon:
                # days = CommonClass.count_working_days()
                attend_rates[i][0] = round(((attend_rates[i][0]/attend_rates[i][1])*100),2)
            elif i==curr_mon:
                attend_rates[i][0] = round(((attend_rates[i][0]/attend_rates[i][1])*100),2)

        months = []
        rates = []

        for i in attend_rates:
            months.append(i)
            rates.append(attend_rates[i][0])


        return months, rates

        # return attend_rates


    ##graph related stuff
    def generate_hex_colors(n, saturation=0.7, value=0.95):
        """Generate n visually distinct hex colors suitable for pie charts."""
        colors = []
        for i in range(n):
            hue = i / n
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            colors.append(hex_color)
        random.shuffle(colors)  # Optional: randomize order
        return colors


    def get_current():
        return datetime.datetime.now()
    
    def get_last_6_months():
        today = datetime.datetime.today()
        months = []
        for i in range(6):
            date = today - relativedelta(months=i)
            months.append((date.month, date.year))
        return months[::-1]    
    
    def count_working_days(month, year):
        total_days = calendar.monthrange(year, month)[1]
        non_sundays = 0
        for day in range(1, total_days + 1):
            if date(year, month, day).weekday() != 6:  # 6 = Sunday
                non_sundays += 1
        return non_sundays

    def count_working_days_current_month():
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        current_day = today.day

        non_sundays = 0
        for day in range(1, current_day + 1):
            if date(year, month, day).weekday() != 6:  # 6 = Sunday
                non_sundays += 1
        return non_sundays



    # def abc():
    #     ab = Attendance.objects.all()[:5]
    #     lst1 = [i.date for  i in ab]
    #     return lst1