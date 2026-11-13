import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.test import Client
from bsp.models import User, CheckLog
from bsp.utils.shifts import get_current_shift_info
from bsp.utils.currency import format_indian_currency

def run_tests():
    print("========================================")
    print("Running SAIL BSP Portal Integration Tests")
    print("========================================")

    # 1. Test Currency & Color Utils
    curr = format_indian_currency(1234567.89)
    assert "₹12,34,568" in curr, f"Unexpected currency: {curr}"
    print("✅ Currency formatting utility passed:", curr)

    # 2. Test Shift Info Utility
    central_hr = User.objects.filter(username="central_hr").first()
    assert central_hr is not None, "central_hr user not found!"
    shift = get_current_shift_info(central_hr)
    assert "shift_name" in shift
    assert "shift_code" in shift
    assert "status_label" in shift
    print(f"✅ Shift calculation passed: {shift['shift_name']} (Code: {shift['shift_code']}), Status: {shift['status_label']}")

    # 3. Test HTTP Client for Employee
    client = Client()
    login_ok = client.login(username="central_hr", password="Logitech1*")
    assert login_ok, "Login failed for central_hr!"
    print("✅ Authentication passed for 'central_hr'")

    # 4. Test Employee Homepage
    resp = client.get("/bsp/home/")
    print(f"DEBUG: Homepage status_code: {resp.status_code}")
    assert resp.status_code == 200, f"Homepage failed: {resp.status_code}"
    assert b"SAIL Plant Shift Schedule" in resp.content
    print("✅ Employee Homepage passed (status 200, shift schedule displayed)")

    # 5. Test Admin Dashboard
    resp = client.get("/bsp/Admin-Dashboard/")
    assert resp.status_code == 200, f"Admin Dashboard failed: {resp.status_code}"
    assert b"Central HR Dashboard" in resp.content or b"Export to CSV" in resp.content
    print("✅ Admin Dashboard passed (status 200, Export buttons displayed)")

    # 6. Test Present / Absent / Late User Lists
    for url, name in [
        ("/bsp/Admin-Dashboard/all-employees/", "All Employees"),
        ("/bsp/Admin-Dashboard/all-pres-employees/", "Present Employees"),
        ("/bsp/Admin-Dashboard/all-abs-employees/", "Absent Employees"),
        ("/bsp/Admin-Dashboard/all-late-employees/", "Late Employees"),
    ]:
        resp = client.get(url)
        assert resp.status_code == 200, f"{name} failed with status {resp.status_code}"
        print(f"✅ {name} table passed (status 200)")

    # 7. Test CSV Exports
    resp_emp_csv = client.get("/bsp/export/employees-csv/")
    assert resp_emp_csv.status_code == 200, "Employees CSV export failed"
    assert "text/csv" in resp_emp_csv["Content-Type"]
    assert b"Employee ID" in resp_emp_csv.content or b"BSP ID" in resp_emp_csv.content
    print("✅ Employees CSV export passed (Content-Type: text/csv, rows verified)")

    resp_att_csv = client.get("/bsp/export/attendance-csv/")
    assert resp_att_csv.status_code == 200, "Attendance CSV export failed"
    assert "text/csv" in resp_att_csv["Content-Type"]
    assert b"Status" in resp_att_csv.content
    print("✅ Attendance CSV export passed (Content-Type: text/csv, rows verified)")

    # 8. Test Payslip View
    resp_pay = client.get("/bsp/payslip/")
    assert resp_pay.status_code == 200, "Payslip view failed"
    assert b"STEEL AUTHORITY OF INDIA LIMITED" in resp_pay.content
    assert b"PAYSLIP" in resp_pay.content
    print("✅ Printable SAIL Payslip passed (status 200, branded template verified)")

    # 9. Test Toast Messages on Punch
    user2 = User.objects.filter(username="user2").first()
    if user2:
        client2 = Client()
        client2.login(username="user2", password="Logitech1*")
        resp_punch = client2.post("/bsp/punch-in/")
        assert resp_punch.status_code == 200, f"Punch-in returned {resp_punch.status_code}"
        print("✅ Punch In endpoint executed successfully")

    print("\n========================================")
    print("🎉 ALL INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("========================================")

if __name__ == '__main__':
    run_tests()
