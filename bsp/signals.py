from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CheckLog, Attendance

@receiver(post_save, sender=CheckLog)
def run_classb_function_on_classa_create(sender, instance, created, **kwargs):
    if created:
        # Get or create a Attendance instance, or call classmethod instead
        b = Attendance()
        b.record_updater(instance)
