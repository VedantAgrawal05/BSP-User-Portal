from datetime import date
from django.db import models

from django.contrib.auth.models import AbstractUser#, User
import datetime, calendar

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
    department_id = models.ForeignKey(DepartmentList, on_delete=models.SET_NULL, null=True)

    # designation = models.CharField(max_length=200)
    designation_id = models.ForeignKey(DesignationList, on_delete=models.SET_NULL, null=True)
    
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
                elif iter.was_present == 1:
                    iter.was_present="Present"
                elif iter.was_present == 2:
                    iter.was_present="Partial Day"
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
            start = date(2025, 5, 25)  # Replace with your desired start date

        # def get_date_list(start_date):
        today = date.today()
        delta = today - start
        dates_list = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]

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

    def get_info(uobj):
        Attendance.absent_days_populator(uobj)
        # recs = Attendance.objects.filter(username=uobj).sort_by('-date')[:35]
        month_dates = Attendance.get_dates()
        present_count = 0
        absent_count = 0
        total_hours = 0

        for iter in month_dates:
            rec = Attendance.objects.filter(username=uobj, date=iter)[0]
            total_hours += rec.hours_worked
            
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
            rec=Attendance.objects.filter(username=uobj, date=dt)[0]
            perc = (rec.hours_worked/8)*100
            as_pe = f"{perc}%"
            weekly_hours.append(as_pe)

        info["weekly_hours"]=weekly_hours

        recent_activities = CheckLog.get_recent_activities(uobj)

        info["recent_activities"]=recent_activities
        info["len_of_recents"]=len(recent_activities)

        return info



    def get_current_week_dates():
        today = date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday
        return [start_of_week + datetime.timedelta(days=i) for i in range((today - start_of_week).days + 1)]

# class PayDetails(models.Model):
#     designation_id = models.ForeignKey(DesignationList, on_delete=models.SET_NULL, null=True)
#     basic_salary= models.DecimalField(max_digits=10, decimal_places=2)
#     allowances = models.DecimalField(max_digits=10, decimal_places=2)
#     deductions = models.DecimalField(max_digits=10, decimal_places=2)
#     net_salary= models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.designation_id} {self.net_salary}"


# class EmployeeDetails(models.Model):
#     username = models.ForeignKey(User, on_delete=models.DELETE)
#     res_address = models.CharField(max_length=300)
#     corr_address = models.CharField(max_length=300)
#     phone_number = models.BigIntegerField()
#     emergency_contact_name = models.CharField(max_length=100)
#     emergency_contact_number = models.BigIntegerField(max_length=100)
    