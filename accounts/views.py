from datetime import datetime,timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializer import SignUpSerializer,InfoSerializer


@api_view(['POST'])
def signup_api(request):
    data = request.data
    signup = SignUpSerializer(data=data)
    if signup.is_valid():
        user = User.objects.filter(username=data['email'])
        if not user.exists():
            User.objects.create(
                username = data['email'],
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                password = make_password(data['password']),
            )
            return Response({'details':'successfully created your account'},
                            status=status.HTTP_200_OK
                    )
        else:
            return Response({'details':'this email is in use please change it'},
                            status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(signup.errors)
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_info(request):
    user = InfoSerializer(request.user).data
    return Response({'data':user})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.username = data['email']

    if user.password != "":
        user.password = make_password(data['password'])
            
    user.save()
    serial = InfoSerializer(user).data
    return Response(serial)

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User,email=data['email'])
    
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)

    user.user_profile.reset_password_token = token
    user.user_profile.reset_password_expire = expire_date
    user.user_profile.save()

    link = f"http://127.0.0.1:8000/accounts/reset_password/{token}/"

    send_mail(
        "Reset Password",
        f"your reset password link : {link}",
        "omar@gmail.com",
        [data['email']]
    )
    return Response({'detail':'sent the mail successfully'})

@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(User,user_profile__reset_password_token = token)

    if data['password'] != data['confirm_password']:
        return Response({'error':'the passwords are not the same '})
    
    if user.user_profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error':'the token had expired'})
    
    user.user_profile.reset_password_token = ""
    user.user_profile.reset_password_expire = None
    user.user_profile.save()

    user.password = make_password(data['password'])
    user.save()

    return Response({'detail':'Reset the Password Successfully'})
