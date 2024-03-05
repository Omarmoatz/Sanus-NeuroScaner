from django.urls import path

from .views import company_info

#  aboutUs/
urlpatterns = [
    path('',company_info)
]
