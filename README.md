# First time stuff (only once)
## Reuirements
* Python installed
* MySQL installed [guide](https://dev.mysql.com/downloads/installer/)
**IMPORTANT**: Note the username and password separately you use during installation 

## After opening the repo folder in VS Code
Run following code in terminal
```
python -m venv venv
```
Next, one of these should work
```
venv\Scripts\activate
venv\Scripts\Activate.bat
```
After this, open a new terminal. VS Code should show a popup about venv activation in bottom right. run the next codes in the new terminal
```
pip install Django python-dateutil mysql-connector
```

Verify installation (should return a number 5.x.x or something like that)
```
py -m django --version
```

### Leave terminal open, and open MySQL Command Line client 
* Ensure you are able to log in using the password you created during installation
* If any issues, reinstall MySQL and repeat step
* Once you are able to see the mysql> prompt it is okay
run below query
```
create database bsp_site_2;
```

Come back to VS Code and go to /app/settings.py file
Scroll down to DATABASES variable (line 85)
change the "USER" and "PASSWORD" key values to your username and password of mysql and save


### Run below commands
```
py manage.py makemigrations
``` 
```
py manage.py migrate

```
after below command, enter your preferred username email and password (note down these username and password as well) (note: password won't be visible when typing)
```
py manage.py createsuperuser
```

### Open MySQL and run below queries one by one
for pasting in mysql use shift + insert if ctrl+v doesn't work
```sql
use bsp_site_2;
```

```sql
INSERT INTO bsp_paydetails (basic_salary, allowances, deductions, net_salary, designation_id) VALUES
(50000.00, 10000.00, 5000.00, 55000.00, 1),
(45000.00, 8000.00, 4000.00, 49000.00, 2),
(60000.00, 15000.00, 7000.00, 68000.00, 3),
(30000.00, 5000.00, 2000.00, 33000.00, 4),
(75000.00, 20000.00, 10000.00, 85000.00, 5),
(55000.00, 9000.00, 3000.00, 61000.00, 6),
(42000.00, 6000.00, 2500.00, 45500.00, 7),
(38000.00, 4000.00, 1800.00, 40200.00, 8),
(67000.00, 12000.00, 6000.00, 73000.00, 9),
(52000.00, 7500.00, 3500.00, 56000.00, 10);
```

```sql
INSERT INTO bsp_employeedetails (
    res_address, 
    corr_address, 
    phone_number, 
    emergency_contact_name, 
    emergency_contact_number, 
    username_id
) VALUES
(
    '123 Park Street, Kolkata, West Bengal',
    '456 Lake Road, Kolkata, West Bengal',
    9876543210,
    'Anita Sharma',
    9123456780,
    1
),
(
    '78 MG Road, Pune, Maharashtra',
    '22 FC Road, Pune, Maharashtra',
    9765432109,
    'Ravi Kulkarni',
    9345678901,
    2
),
(
    '11 Banjara Hills, Hyderabad, Telangana',
    '35 Jubilee Hills, Hyderabad, Telangana',
    9988776655,
    'Suma Reddy',
    9001234567,
    3
),
(
    '9 Sector 21, Chandigarh',
    '15 Sector 18, Chandigarh',
    9871201234,
    'Amit Verma',
    9812345678,
    4
),
(
    '5 Indira Nagar, Lucknow, Uttar Pradesh',
    '8 Gomti Nagar, Lucknow, Uttar Pradesh',
    9911223344,
    'Priya Singh',
    9321654321,
    5
);
```

```sql
INSERT INTO bsp_departmentlist (department_id, department_name) VALUES
(0, 'Not Assigned'),
(1, 'Human Resources'),
(2, 'Finance'),
(3, 'Engineering'),
(4, 'Marketing'),
(5, 'Sales'),
(6, 'Research and Development'),
(7, 'Customer Support'),
(8, 'Legal'),
(9, 'IT Services'),
(10, 'Operations');
```

```sql
INSERT INTO bsp_designationList (designation_id, designation_name) VALUES
(0, 'Not Assigned'),
(1, 'Manager'),
(2, 'Team Lead'),
(3, 'Software Engineer'),
(4, 'Accountant'),
(5, 'HR Executive'),
(6, 'Sales Executive'),
(7, 'Legal Advisor'),
(8, 'Research Analyst'),
(9, 'Support Specialist'),
(10, 'Operations Coordinator');
```

**Important**: In the below query at the last replace ```<username>``` with the username you used while creating the superuser, with no extra spaces
```sql
update auth_user set first_name="rajesh", last_name="singh", birthday="2000-01-01", department_id_id=1, designation_id_id=1, is_dept_hr=1 where username="<username>";
```

# Start sequence (to be done everytime server is to be started)
activate venv (only when opening/restarting vscode)
```
venv\Scripts\activate
venv\Scripts\Activate.bat
```
server
```
py manage.py runserver
```
click on the link or go to the localhost and login with the username and password of superuser created

### optional
set workspace python interpreter to the venv so whenever you open the folder you just have to open a new terminal, instead of using the activation script first. (note: this is finicky and doesn't always work very well)
* Ctrl + Shift + P in VSCode
* type select interpreter
* Click on the Python: Select Interpreter option 
* Choose the one with venv in the brackets

# Common errors:
* 2002, "Can't connect to server on 'localhost' (10061)": To fix, type and go to services in search menu, find MySQL, right click & start