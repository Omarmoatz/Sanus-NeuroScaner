from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.signup_api ),
    path('get_info', views.user_info ),
    path('update', views.update_profile ),
    path('forgot_password/', views.forgot_password ),
    path('reset_password/<str:token>/', views.reset_password ),
]
