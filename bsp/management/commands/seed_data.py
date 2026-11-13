import datetime
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bsp.models import DepartmentList, DesignationList, PayDetails, EmployeeDetails, CheckLog, Attendance

User = get_user_model()

DEPARTMENTS = [
    (0, "Not Assigned"),
    (1, "Human Resources"),
    (2, "Finance"),
    (3, "Engineering"),
    (4, "Marketing"),
    (5, "Sales"),
    (6, "Research and Development"),
    (7, "Customer Support"),
    (8, "Legal"),
    (9, "IT Services"),
    (10, "Operations"),
]

DESIGNATIONS = [
    (0, "Not Assigned"),
    (1, "Manager"),
    (2, "Team Lead"),
    (3, "Software Engineer"),
    (4, "Accountant"),
    (5, "HR Executive"),
    (6, "Sales Executive"),
    (7, "Legal Advisor"),
    (8, "Research Analyst"),
    (9, "Support Specialist"),
    (10, "Operations Coordinator"),
]

PAY_SLABS = [
    (1, 50000.00, 10000.00, 5000.00, 55000.00),
    (2, 45000.00, 8000.00, 4000.00, 49000.00),
    (3, 60000.00, 15000.00, 7000.00, 68000.00),
    (4, 30000.00, 5000.00, 2000.00, 33000.00),
    (5, 75000.00, 20000.00, 10000.00, 85000.00),
    (6, 55000.00, 9000.00, 3000.00, 61000.00),
    (7, 42000.00, 6000.00, 2500.00, 45500.00),
    (8, 38000.00, 4000.00, 1800.00, 40200.00),
    (9, 67000.00, 12000.00, 6000.00, 73000.00),
    (10, 52000.00, 7500.00, 3500.00, 56000.00),
]

CORE_USERS = [
    {
        "username": "central_hr",
        "first_name": "Priya",
        "last_name": "Sharma",
        "email": "central_hr@bsp.com",
        "dept_id": 1,
        "desg_id": 1,
        "is_superuser": True,
        "is_staff": True,
        "is_dept_hr": True,
        "phone": 9876512345,
        "res_address": "Sector 2, Bhilai, Chhattisgarh",
        "corr_address": "Sector 2, Bhilai, Chhattisgarh",
        "emer_name": "Rajesh Sharma",
        "emer_phone": 9876512340,
    },
    {
        "username": "hr_user",
        "first_name": "Anita",
        "last_name": "Sharma",
        "email": "hr@gmail.com",
        "dept_id": 1,
        "desg_id": 5,
        "is_superuser": False,
        "is_staff": True,
        "is_dept_hr": True,
        "phone": 9123456780,
        "res_address": "Sector 4, Bhilai, Chhattisgarh",
        "corr_address": "Sector 4, Bhilai, Chhattisgarh",
        "emer_name": "Sunil Sharma",
        "emer_phone": 9123456789,
    },
    {
        "username": "user2",
        "first_name": "Ravi",
        "last_name": "Kulkarni",
        "email": "user2@gmail.com",
        "dept_id": 3,
        "desg_id": 3,
        "is_superuser": False,
        "is_staff": False,
        "is_dept_hr": False,
        "phone": 9765432109,
        "res_address": "Civic Centre, Bhilai, Chhattisgarh",
        "corr_address": "Civic Centre, Bhilai, Chhattisgarh",
        "emer_name": "Asha Kulkarni",
        "emer_phone": 9765432100,
    },
    {
        "username": "archit",
        "first_name": "Archit",
        "last_name": "Gupta",
        "email": "archit@test.com",
        "dept_id": 9,
        "desg_id": 1,
        "is_superuser": True,
        "is_staff": True,
        "is_dept_hr": True,
        "phone": 9811223344,
        "res_address": "Sector 6, Bhilai, Chhattisgarh",
        "corr_address": "Sector 6, Bhilai, Chhattisgarh",
        "emer_name": "V. Gupta",
        "emer_phone": 9811223340,
    },
    {
        "username": "amit_verma",
        "first_name": "Amit",
        "last_name": "Verma",
        "email": "amit.verma@bsp.com",
        "dept_id": 10,
        "desg_id": 10,
        "is_superuser": False,
        "is_staff": False,
        "is_dept_hr": False,
        "phone": 9871201234,
        "res_address": "Sector 1, Bhilai, Chhattisgarh",
        "corr_address": "Sector 1, Bhilai, Chhattisgarh",
        "emer_name": "Sanjay Verma",
        "emer_phone": 9812345678,
    },
    {
        "username": "suma_reddy",
        "first_name": "Suma",
        "last_name": "Reddy",
        "email": "suma.reddy@bsp.com",
        "dept_id": 2,
        "desg_id": 4,
        "is_superuser": False,
        "is_staff": False,
        "is_dept_hr": False,
        "phone": 9988776655,
        "res_address": "Sector 9, Bhilai, Chhattisgarh",
        "corr_address": "Sector 9, Bhilai, Chhattisgarh",
        "emer_name": "K. Reddy",
        "emer_phone": 9001234567,
    },
]

class Command(BaseCommand):
    help = "Seeds database with SAIL BSP departments, designations, pay details, users, and attendance records"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🌱 Starting database seeding..."))

        # 1. Departments
        for d_id, d_name in DEPARTMENTS:
            DepartmentList.objects.update_or_create(
                department_id=d_id,
                defaults={"department_name": d_name}
            )
        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(DEPARTMENTS)} departments."))

        # 2. Designations
        for des_id, des_name in DESIGNATIONS:
            DesignationList.objects.update_or_create(
                designation_id=des_id,
                defaults={"designation_name": des_name}
            )
        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(DESIGNATIONS)} designations."))

        # 3. Pay Details
        for des_id, basic, allow, deduct, net in PAY_SLABS:
            desg_obj = DesignationList.objects.get(designation_id=des_id)
            PayDetails.objects.update_or_create(
                designation_id=desg_obj,
                defaults={
                    "basic_salary": basic,
                    "allowances": allow,
                    "deductions": deduct,
                    "net_salary": net,
                }
            )
        self.stdout.write(self.style.SUCCESS(f"✅ Loaded {len(PAY_SLABS)} pay slabs."))

        # 4. Users and Employee Details
        created_users = []
        for udata in CORE_USERS:
            dept_obj = DepartmentList.objects.get(department_id=udata["dept_id"])
            desg_obj = DesignationList.objects.get(designation_id=udata["desg_id"])
            
            user, created = User.objects.get_or_create(
                username=udata["username"],
                defaults={
                    "email": udata["email"],
                    "first_name": udata["first_name"],
                    "last_name": udata["last_name"],
                    "department_id": dept_obj,
                    "designation_id": desg_obj,
                    "is_superuser": udata["is_superuser"],
                    "is_staff": udata["is_staff"],
                    "is_dept_hr": udata["is_dept_hr"],
                    "birthday": datetime.date(1995, 1, 1),
                    "date_joined": datetime.date(2025, 1, 1),
                }
            )
            user.department_id = dept_obj
            user.designation_id = desg_obj
            user.is_superuser = udata["is_superuser"]
            user.is_staff = udata["is_staff"]
            user.is_dept_hr = udata["is_dept_hr"]
            user.set_password("Logitech1*")
            user.save()

            EmployeeDetails.objects.update_or_create(
                username=user,
                defaults={
                    "phone_number": udata["phone"],
                    "res_address": udata["res_address"],
                    "corr_address": udata["corr_address"],
                    "emergency_contact_name": udata["emer_name"],
                    "emergency_contact_number": udata["emer_phone"],
                }
            )
            created_users.append(user)

        self.stdout.write(self.style.SUCCESS(f"✅ Synced {len(CORE_USERS)} test users with password 'Logitech1*'."))

        # 5. Seed Attendance and CheckLogs for rich charts
        today = datetime.date.today()
        for user in created_users:
            # Check-in today
            CheckLog.objects.get_or_create(
                username=user,
                date=today,
                action_id=1,
                defaults={
                    "time": datetime.time(9, 5, 0),
                    "shift": "G",
                }
            )
            # Past 30 days attendance records
            for d in range(1, 31):
                past_date = today - datetime.timedelta(days=d)
                if past_date.weekday() != 6:  # Skip Sundays
                    Attendance.objects.get_or_create(
                        username=user,
                        date=past_date,
                        defaults={
                            "was_present": 1 if random.random() > 0.15 else 0,
                            "shift": "G",
                            "hours_worked": 8.0,
                        }
                    )

        self.stdout.write(self.style.SUCCESS("✅ Attendance history & check-in logs generated."))
        self.stdout.write(self.style.SUCCESS("🎉 Seeding complete! The database is ready for demonstration."))

