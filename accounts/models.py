from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50,blank=True,default="")
    reset_password_expire = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(
            user = instance,
        )

class DoctorProfile(models.Model):
    user = models.OneToOneField( User, related_name='user_doctor', on_delete=models.CASCADE)
    img = models.ImageField( upload_to='doctor img', blank=True, null=True)
    master_degree = models.ImageField( upload_to='master degree')
    phd_degree = models.ImageField( upload_to='phd degree', blank=True, null=True)
    clink_location = models.CharField( max_length=500)
    medical_center = models.TextField( max_length=1000, blank=True, null=True)
    syndicate_card = models.ImageField( upload_to='syndicate card')

    def __str__(self):
        return str(self.user)

class PatientProfile(models.Model):
    user = models.OneToOneField( User, related_name='user_patient', on_delete=models.CASCADE)
    img = models.ImageField( upload_to='patient img', blank=True, null=True)
    doctor = models.ForeignKey( DoctorProfile, related_name='doctor_patient', on_delete=models.CASCADE)
    date_of_birth = models.DateField( blank=True, null=True)
    chronic_diseases = models.TextField( max_length=1000, blank=True, null=True)
    x_ray = models.ImageField( upload_to='x_ray', blank=True, null=True)
    symptoms = models.TextField( max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.user)
