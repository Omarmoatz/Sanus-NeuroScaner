from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PatientProfile, DoctorProfile, CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        if instance.user_type == 'Patient':
            PatientProfile.objects.create(user=instance)
        elif instance.user_type == 'Doctor':
            DoctorProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'Patient' and hasattr(instance, 'patientprofile'):
        instance.patientprofile.save()
    elif instance.user_type == 'Doctor' and hasattr(instance, 'doctorprofile'):
        instance.doctorprofile.save()