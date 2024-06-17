from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Subquery , Q , OuterRef
from django.shortcuts import get_object_or_404

from accounts.models import PatientProfile, CustomUser, DoctorProfile
from accounts.serializer import PatientInfoSerializer, DoctorInfoSerializer
from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatList(generics.ListAPIView):
    # finding all chats between me and other users
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # finding last messege between me and other users and order them then put there id in list 
        latest_messege = ChatMessage.objects.filter(
            Q( sender= OuterRef('id'), receiver= user ) |
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
    

class GetMesseges(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = self.request.user 
        receiver_id = self.kwargs['receiver_id']

        messeges = ChatMessage.objects.filter(
            sender__in = [ sender_id , receiver_id ],
            receiver__in = [ sender_id , receiver_id ]
        )
        return messeges

class SendMessege(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.kwargs['pk']
        receiver = get_object_or_404(CustomUser, id=receiver_id)
        sender = self.request.user

        serializer.save(sender= sender, receiver= receiver)

class SearchPatient(generics.ListAPIView):
    serializer_class = PatientInfoSerializer
    queryset = PatientProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user 
        username = self.kwargs['username']

        seached_user = PatientProfile.objects.filter(
            Q(user__username__icontains = username) |
            Q(user__email__icontains = username) |
            Q(user__last_name__icontains = username) |
            Q(user__first_name__icontains = username) &
            ~Q(user = user) 
        )

        if not seached_user.exists():
            return Response({'details':f'No Patient found with {username}'},
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(seached_user, many=True)
        return Response(serializer.data) 
    
class SearchDoctor(generics.ListAPIView):
    serializer_class = DoctorInfoSerializer
    queryset = DoctorProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user 
        username = self.kwargs['username']

        seached_user = DoctorProfile.objects.filter(
            Q(user__username__icontains = username) |
            Q(user__email__icontains = username) |
            Q(user__last_name__icontains = username) |
            Q(user__first_name__icontains = username) &
            ~Q(user = user) 
        )

        if not seached_user.exists():
            return Response({'details':f'No doctor found with {username}'},
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(seached_user, many=True)
        return Response(serializer.data)