from django.urls import path
from . import views

#   accounts/
urlpatterns = [
    path('patient-signup/', views.patient_signup ),
    path('doctor-signup/', views.doctor_signup ),
    path('doctor-activation/<str:username>/', views.activate_doctor_profile ),
    path('login/', views.login ),
    path('get_info/', views.user_info ),
    path('update/', views.update_profile ),
    path('forgot_password/', views.forgot_password ),
    path('reset_password/<str:token>/', views.reset_password ),
]
