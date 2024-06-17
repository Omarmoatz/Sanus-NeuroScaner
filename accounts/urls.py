from django.urls import path
from . import views

#   accounts/
urlpatterns = [
    path('patient-signup/', views.patient_signup ),
    path('doctor-signup/', views.doctor_signup ),
    path('doctor-activation/<str:username>/', views.activate_doctor_profile ),
    path('login/', views.login ),
    path('get_info/', views.profile_info ),
    path('patient_list/', views.patient_list ),
    path('doctor_list/', views.doctor_list ),
    path('update_profile/', views.update_profile ),
    path('forgot_password/', views.forgot_password ),
    path('reset_password/<str:token>/', views.reset_password ),

    # generic api 
    path('patient_detail/<int:pk>/', views.PatientProfileDetail.as_view()),
    path('doctor_detail/<int:pk>/', views.DoctorProfileDetail.as_view()),
]
