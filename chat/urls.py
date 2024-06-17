from django.urls import path

from . import views

app_name = 'chat/'

#  chats/
urlpatterns = [
    path('', views.ChatList.as_view(), name='chat_list' ),
    path('<receiver_id>/', views.GetMesseges.as_view(), name='messeges' ),
    path('send_messege/<int:pk>/', views.SendMessege.as_view(), name='send_messege' ),
    path('search_patient/<username>/', views.SearchPatient.as_view(), name='search_patient'),
    path('search_doctor/<username>/', views.SearchDoctor.as_view(), name='search_doctor')
]
