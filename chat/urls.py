from django.urls import path

from . import views

app_name = 'chat'

#  chats/
urlpatterns = [
    path('all_chats/', views.ChatList.as_view(), name='chat_list' ),
]
