import datetime

def get_current_shift_info(user_obj=None):
    """
    Computes current SAIL plant shift details and today's punch status for an employee.
    SAIL Plant Shifts:
      - Shift A (Morning): 06:00 to 14:00
      - Shift G (General): 09:00 to 17:00
      - Shift B (Evening): 14:00 to 22:00
      - Shift C (Night): 22:00 to 06:00
    """
    now = datetime.datetime.now()
    current_time = now.time()
    hour = current_time.hour

    if 6 <= hour < 14:
        if 9 <= hour < 17:
            current_shift = "General Shift (G)"
            shift_code = "G"
            shift_timing = "09:00 AM - 05:00 PM"
        else:
            current_shift = "Shift A (Morning)"
            shift_code = "A"
            shift_timing = "06:00 AM - 02:00 PM"
    elif 14 <= hour < 22:
        current_shift = "Shift B (Evening)"
        shift_code = "B"
        shift_timing = "02:00 PM - 10:00 PM"
    else:
        current_shift = "Shift C (Night)"
        shift_code = "C"
        shift_timing = "10:00 PM - 06:00 AM"

    today_date_str = now.strftime("%A, %d %B %Y")

    result = {
        "shift_name": current_shift,
        "shift_code": shift_code,
        "shift_timing": shift_timing,
        "today_date": today_date_str,
        "current_time": now.strftime("%I:%M %p"),
        "punched_in": False,
        "punch_in_time": None,
        "punched_out": False,
        "punch_out_time": None,
        "status_label": "Punch In Pending",
        "status_class": "status-pending",
        "status_color": "#ed8936",
    }

    if user_obj:
        from bsp.models import CheckLog
        curr_date = CheckLog.get_current_date()
        pin = CheckLog.objects.filter(username=user_obj, date=curr_date, action_id=1).order_by('-time').first()
        pout = CheckLog.objects.filter(username=user_obj, date=curr_date, action_id=2).order_by('-time').first()

        if pin:
            result["punched_in"] = True
            result["punch_in_time"] = pin.time.strftime("%I:%M %p") if hasattr(pin.time, 'strftime') else str(pin.time)
        if pout:
            result["punched_out"] = True
            result["punch_out_time"] = pout.time.strftime("%I:%M %p") if hasattr(pout.time, 'strftime') else str(pout.time)

        if result["punched_in"] and result["punched_out"]:
            result["status_label"] = "Shift Completed"
            result["status_class"] = "status-completed"
            result["status_color"] = "#48bb78"
        elif result["punched_in"]:
            result["status_label"] = "On Duty (Active)"
            result["status_class"] = "status-active"
            result["status_color"] = "#38b2ac"
        else:
            result["status_label"] = "Punch In Pending"
            result["status_class"] = "status-pending"
            result["status_color"] = "#ed8936"

    return result

