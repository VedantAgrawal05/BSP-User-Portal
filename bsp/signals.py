from datetime import datetime, timedelta, time
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import User, CheckLog, Attendance

# @receiver(post_save, sender=CheckLog)
# def run_classb_function_on_classa_create(sender, instance, created, **kwargs):
#     if created:
#         # Get or create a Attendance instance, or call classmethod instead
#         b = Attendance()
#         b.record_updater(instance)


from .middleware import get_current_request
from django.db import models
from .models import User, CheckLog, Attendance

FMT = '%H:%M:%S'
dummy_date = datetime(2000, 1, 3)
"""Updating attendance record on punchout action """

@receiver(post_save, sender=CheckLog)
def record_updater(sender, instance, created, **kwargs):
        request = get_current_request()
        curr_user = getattr(request, 'user', None)
        # action_id = getattr(request, 'action_id', None)
        # shift = getattr(request, 'shift', None)
        # curr_date = getattr(request, 'date', None)
        # curr_time = getattr(request, 'time', None)
        normal_shifts = ["A","B","G"]   

        user_obj= User.objects.get(username=curr_user)
        latest_rec= CheckLog.objects.filter(username=user_obj).order_by("-date","-time")
        action_id = latest_rec[0].action_id
        shift = latest_rec[0].shift
        curr_date = latest_rec[0].date
        curr_time = latest_rec[0].time



        #only need to do when action is punch out
            # print(action_id)
        if action_id==2:
                # print("prnt")
                #if morning, second or general shift only
                if shift in normal_shifts:
                    user_obj= User.objects.get(username=curr_user)
                    last_actions= CheckLog.objects.filter(username=user_obj, date=curr_date, action_id=1, shift=shift).order_by("time")
                    if last_actions:
                        punch_in_time = last_actions[0].time
                        # punch_in_time = punch_in_rec.time
                        dt_curr = datetime.combine(dummy_date, curr_time)
                        dt_punch = datetime.combine(dummy_date, punch_in_time)
                        # tdelta = datetime.strptime(curr_time, FMT) - datetime.strptime(punch_in_time, FMT)
                        tdelta = dt_curr - dt_punch
                        seconds = tdelta.total_seconds()
                        # m, s = divmod(seconds, 60)
                        # hours, m = divmod(m, 60)
                        total_hours=seconds/3600
                        #rounding to nearest 0.25 hour (15 min)
                        hours = (total_hours//0.25)*0.25

                        new_rec=Attendance(username=user_obj, date=curr_date, was_present=1, shift=shift,hours_worked= hours)
                        new_rec.save()
                
                #default shift or for partial day, hours worked will still count
                elif shift=="D":
                    user_obj= User.objects.get(username=curr_user)
                    last_actions= CheckLog.objects.filter(username=user_obj, date=curr_date, action_id=1, shift=shift).order_by("time")
                    if last_actions:
                        punch_in_time = last_actions[0].time
                        # punch_in_time = punch_in_rec.time

                        dt_curr = datetime.combine(dummy_date, curr_time)
                        dt_punch = datetime.combine(dummy_date, punch_in_time)
                        # tdelta = datetime.strptime(curr_time, FMT) - datetime.strptime(punch_in_time, FMT)
                        tdelta = dt_curr - dt_punch
                        seconds = tdelta.total_seconds()
                        # m, s = divmod(seconds, 60)
                        # hours, m = divmod(m, 60)
                        total_hours=seconds/3600
                        #rounding to nearest 0.25 hour (15 min)
                        hours = (total_hours//0.25)*0.25

                        new_rec=Attendance(username=user_obj, date=curr_date, was_present=2, shift=shift,hours_worked= hours)
                        new_rec.save()
                
                #night shift requires more logic
                elif shift=="C":
                    user_obj= User.objects.get(username=curr_user)
                    prev_date = curr_date - timedelta(days=1)
                    last_actions= CheckLog.objects.filter(username=user_obj, date=prev_date, action_id=1, shift=shift).order_by("time")
                    if last_actions:
                        punch_in_time = last_actions[0].time
                        # punch_in_time = punch_in_rec.time
                        time1 = time(23,59,0)
                        time2 = time(0,1,0)
                        dt_1 = datetime.combine(dummy_date, time1)
                        dt_2 = datetime.combine(dummy_date, time2)
                        
                        dt_curr = datetime.combine(dummy_date, curr_time)
                        dt_punch = datetime.combine(dummy_date, punch_in_time)
                        # tdelta = datetime.strptime(curr_time, FMT) - datetime.strptime(punch_in_time, FMT)
                        td_1 = dt_curr - dt_2
                        td_2 = dt_1 - dt_punch

                        tdelta = td_1.total_seconds() + td_2.total_seconds() + 2

                        seconds = tdelta.total_seconds()
                        # m, s = divmod(seconds, 60)
                        # hours, m = divmod(m, 60)
                        total_hours=seconds/3600
                        #rounding to nearest 0.25 hour (15 min)
                        hours = (total_hours//0.25)*0.25

                        new_rec=Attendance(username=user_obj, date=prev_date, was_present=1, shift=shift,hours_worked= hours)
                        new_rec.save()

        # print(f"User {user} triggered creation of {instance}")
