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
        

