from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .forms import SignUpForm
from .models import User, DepartmentList, DesignationList


class DepartmentListAdmin(admin.ModelAdmin):
    list_display = ['department_id', 'department_name']

class DesignationListAdmin(admin.ModelAdmin):
    list_display = ['designation_id', 'designation_name']

admin.site.register(DepartmentList,DepartmentListAdmin)
admin.site.register(DesignationList,DesignationListAdmin)

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = SignUpForm
    model = User
    list_display = ["id", "username", "email", "is_staff",]

admin.site.register(User, CustomUserAdmin)