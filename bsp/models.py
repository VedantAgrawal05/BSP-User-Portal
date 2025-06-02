from django.db import models
from django.contrib.auth.models import AbstractUser#, User
import datetime

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


#similar to checklog, 1 is used to represent present. no entry or 0 signifies absent
class Attendance(models.Model):
    username=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date=models.DateField(default=datetime.date.today())
    was_present=models.PositiveSmallIntegerField("Present or Absent", default=0)
    shift=models.CharField(max_length=1, null=True, default="D")


    def __str__(self):
        return f"{self.username} {self.was_present}"
    

    def record_updater(self, instance):
        print("yoooo")

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
    