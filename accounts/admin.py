from django.contrib import admin
from .models import PatientProfile,DoctorProfile,CustomUser

admin.site.register(CustomUser)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
