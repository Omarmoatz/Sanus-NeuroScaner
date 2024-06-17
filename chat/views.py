from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Subquery , Q , OuterRef

from .models import ChatMessage, CustomUser
from .serializers import ChatMessageSerializer

class ChatList(generics.ListAPIView):
    # finding all chats between me and other users
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # finding last messege between me and other users and order them then put there id in list 
        latest_messege = ChatMessage.objects.filter(
            Q( sender= OuterRef('id'), recevier= user ) |
            Q( sender= user, receiver= OuterRef('id') )
        ).order_by('-id')[:1].values_list('id', flat=True)

        # finding all the users that i have sent or received messege from them 
        related_users = CustomUser.objects.filter(
            Q( sent_messege__receiver= user ) |
            Q( received_messege__sender= user )
        ).distinct().annotate(
            last_messege = Subquery(latest_messege)
        ).values_list('last_messege' , flat=True )

        # filter chats to bring all ids with the following subquery 
        messege = ChatMessage.objects.filter(
            id__in = Subquery(related_users)
        ).order_by('-id')

        return messege
    