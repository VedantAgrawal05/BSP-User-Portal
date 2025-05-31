# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# # from django.contrib.auth.models import User
# from .models import User, DepartmentList, DesignationList

# class SignUpForm(UserCreationForm):
#     # depts = DepartmentList.objects.all()
#     # departments = DepartmentList.objects.values_list('department_id', 'department_name')
#     # nested_list = [ [dept] for dept in departments ]
#     def get_dept_tuples():
#         depts= DepartmentList.objects.all()
#         lst1=[]
#         for d in depts:
#             lst2=[d.department_id, d.department_name]
#             lst1.append(lst2)
#             lst2=[]
        
#         return lst1


#     def get_desig_tuples():
#         desg= DesignationList.objects.all()
#         lst1=[]
#         for d in desg:
#             lst2=[d.designation_id, d.designation_name]
#             lst1.append(lst2)
#             lst2=[]
        
#         return lst1

#     first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
#     last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
#     email = forms.EmailField(max_length=254, help_text="Required, please enter a valid email address")
#     department = forms.ChoiceField(
#         choices=get_dept_tuples()
#     )
#     designation = forms.ChoiceField(
#         choices=get_desig_tuples()
#     )
#     birthday = forms.DateField()
#     date_joined = forms.DateField()

# # 
#     is_dept_hr = forms.CheckboxInput()
#     is_read_only_superuser = forms.CheckboxInput()

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', "department", "designation", "birthday", "date_joined", "is_dept_hr", "is_read_only_superuser")

    

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DepartmentList, DesignationList
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.forms.widgets import PasswordInput, TextInput

# class CustomLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({
#             'placeholder': 'Username'
#         })
#         self.fields['password'].widget.attrs.update({
#             'placeholder': 'Password'
#         })

# class CustomAuthForm(AuthenticationForm):
#     username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
#     password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))

class MyAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}) 
        self.fields['password'].label = False



# class CustomLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields['username'].widget.attrs.update({
#             'placeholder': 'Username',
#             'class': 'form-input',
#         })

#         self.fields['password'].widget.attrs.update({
#             'placeholder': 'Password',
#             'class': 'form-input',
#         })


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    email = forms.EmailField(max_length=254, help_text="Required, please enter a valid email address")
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-bday'}))
    date_joined = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-joindt'}))
    is_dept_hr = forms.BooleanField(required=False)
    is_read_only_superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
            'birthday', 'date_joined',
            'is_dept_hr', 'is_read_only_superuser'
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['department'] = forms.ChoiceField(
            choices=[(d.department_id, d.department_name) for d in DepartmentList.objects.all()]
        )
        self.fields['designation'] = forms.ChoiceField(
            choices=[(d.designation_id, d.designation_name) for d in DesignationList.objects.all()]
        )
