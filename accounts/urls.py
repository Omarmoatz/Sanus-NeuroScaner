from django.urls import path
from . import views

#   accounts/
urlpatterns = [
    path('signup/', views.signup_api ),
    path('login/', views.login ),
    path('get_info/', views.user_info ),
    path('update/', views.update_profile ),
    path('forgot_password/', views.forgot_password ),
    path('reset_password/<str:token>/', views.reset_password ),
]
