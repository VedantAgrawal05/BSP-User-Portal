from datetime import datetime, timedelta, time
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CheckLog, Attendance

FMT = '%H:%M:%S'
dummy_date = datetime(2000, 1, 3)

@receiver(post_save, sender=CheckLog)
def record_updater(sender, instance, created, **kwargs):
    """
    Automatically updates the Attendance record when a Punch-out (action_id=2) occurs.
    Uses instance fields directly for thread-safety and compatibility with background/CLI jobs.
    """
    if not created or instance.action_id != 2:
        return

    user_obj = instance.username
    if not user_obj:
        return

    shift = instance.shift
    curr_date = instance.date
    curr_time = instance.time
    normal_shifts = ["A", "B", "G"]

    # Morning, afternoon, or general shifts
    if shift in normal_shifts:
        last_actions = CheckLog.objects.filter(
            username=user_obj, date=curr_date, action_id=1, shift=shift
        ).order_by("time")
        if last_actions.exists():
            punch_in_time = last_actions.first().time
            dt_curr = datetime.combine(dummy_date, curr_time)
            dt_punch = datetime.combine(dummy_date, punch_in_time)
            seconds = (dt_curr - dt_punch).total_seconds()
            total_hours = max(0, seconds / 3600)
            hours = (total_hours // 0.25) * 0.25

            Attendance.objects.update_or_create(
                username=user_obj,
                date=curr_date,
                defaults={"was_present": 1, "shift": shift, "hours_worked": hours}
            )

    # Default / partial day shift
    elif shift == "D":
        last_actions = CheckLog.objects.filter(
            username=user_obj, date=curr_date, action_id=1, shift=shift
        ).order_by("time")
        if last_actions.exists():
            punch_in_time = last_actions.first().time
            dt_curr = datetime.combine(dummy_date, curr_time)
            dt_punch = datetime.combine(dummy_date, punch_in_time)
            seconds = (dt_curr - dt_punch).total_seconds()
            total_hours = max(0, seconds / 3600)
            hours = (total_hours // 0.25) * 0.25

            Attendance.objects.update_or_create(
                username=user_obj,
                date=curr_date,
                defaults={"was_present": 2, "shift": shift, "hours_worked": hours}
            )

    # Night shift (crosses midnight)
    elif shift == "C":
        prev_date = curr_date - timedelta(days=1)
        last_actions = CheckLog.objects.filter(
            username=user_obj, date=prev_date, action_id=1, shift=shift
        ).order_by("time")
        if last_actions.exists():
            punch_in_time = last_actions.first().time
            time1 = time(23, 59, 0)
            time2 = time(0, 1, 0)
            dt_1 = datetime.combine(dummy_date, time1)
            dt_2 = datetime.combine(dummy_date, time2)
            dt_curr = datetime.combine(dummy_date, curr_time)
            dt_punch = datetime.combine(dummy_date, punch_in_time)

            td_1 = dt_curr - dt_2
            td_2 = dt_1 - dt_punch
            seconds = td_1.total_seconds() + td_2.total_seconds() + 2
            total_hours = max(0, seconds / 3600)
            hours = (total_hours // 0.25) * 0.25

            Attendance.objects.update_or_create(
                username=user_obj,
                date=prev_date,
                defaults={"was_present": 1, "shift": shift, "hours_worked": hours}
            )
