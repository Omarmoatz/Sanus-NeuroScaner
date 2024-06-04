from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
    )

    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=400)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
    

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_doctor', on_delete=models.CASCADE)
    img = models.ImageField( upload_to='doctor img', blank=True, null=True)
    master_degree = models.ImageField( upload_to='master degree', blank=True, null=True)
    phd_degree = models.ImageField( upload_to='phd degree', blank=True, null=True)
    clink_location = models.CharField( max_length=500, blank=True, null=True)
    medical_center = models.TextField( max_length=1000, blank=True, null=True)
    syndicate_card = models.ImageField( upload_to='syndicate card', blank=True, null=True)
    reset_password_token = models.CharField(max_length=50, blank=True, default="")
    reset_password_expire_date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} - Doctor Profile"
    

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_patient', on_delete=models.CASCADE)
    img = models.ImageField( upload_to='patient img', blank=True, null=True)
    doctor = models.ForeignKey( DoctorProfile, related_name='doctor_patient', on_delete=models.CASCADE, blank=True, null=True)
    date_of_birth = models.DateField( blank=True, null=True)
    chronic_diseases = models.TextField( max_length=1000, blank=True, null=True)
    x_ray = models.ImageField( upload_to='x_ray', blank=True, null=True)
    symptoms = models.TextField( max_length=1000, blank=True, null=True)
    reset_password_token = models.CharField(max_length=50, blank=True, default="")
    reset_password_expire_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Patient Profile"


