from datetime import datetime,timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.decorators import api_view,permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .serializer import PatientInfoSerializer, DoctorInfoSerializer, SignUpSerializer, DoctorProfileSerializer ,LoginSerializer
from .models import CustomUser, DoctorProfile ,PatientProfile


@api_view(['POST'])
def patient_signup(request):
    data = request.data
    signup = SignUpSerializer(data=data)
    if signup.is_valid():    
            CustomUser.objects.create(
                username = data['username'],
                email = data['email'],
                password = make_password(data['password']),
                user_type = 'Patient'
            )
            return Response({'details':'successfully created your account'},
                            status=status.HTTP_200_OK
                    )
    else:
        return Response(signup.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def doctor_signup(request):
    data = request.data
    signup = SignUpSerializer(data=data)
    username = data['username']
    if signup.is_valid():
        CustomUser.objects.create(
            username = username,
            email = data['email'],
            password = make_password(data['password']),
            user_type = 'Doctor',
            is_active = False
        )
        link = f"http://127.0.0.1:8000/accounts/doctor-activation/{username}/"

        send_mail(
            "acivate your account",
            f"follow this link to activate your account : {link}",
            "omar.moataz@gmail.com",
            [data['email']]
        )
        return Response({'Details':'Successfully created your account. please follow the link to activate your account '},
                            status=status.HTTP_200_OK)
    else:
        return Response(signup.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def activate_doctor_profile(request,username):
    '''
        how to get username:
            1- by sending it in the url
            2- make the user enter it again 
            3- The username can be sent in the URL and the user will enter it again to confirm.
    '''
    data = request.data
    try:
        user = CustomUser.objects.get(username=username)
        if user.user_type != 'Doctor':
            return Response({'detail': 'User is not a doctor'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DoctorProfileSerializer(data=data)
        if serializer.is_valid(): 
                profile = user.user_doctor
                profile.img = data.get('img', profile.img)
                profile.master_degree = data.get('master_degree', profile.master_degree)
                profile.phd_degree = data.get('phd_degree', profile.phd_degree)
                profile.clink_location = data.get('clink_location', profile.clink_location)
                profile.medical_center = data.get('medical_center', profile.medical_center)
                profile.syndicate_card = data.get('syndicate_card', profile.syndicate_card)
                profile.save()

                user.is_active = True
                user.save()
                return Response({'details':'Activated your account successfully'},
                                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        user = CustomUser.objects.filter(username=data['username'])
        if user.exists():           
            password = data['password']
            if user.get().check_password(password):
                return Response({'info':'loged in successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error":"Wrong Password"},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error":"This Username Does not exist"},
                            status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile_info(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.user_type == 'Patient':
        try:
            patient_profile = PatientProfile.objects.get(user=request.user)
        except patient_profile.DoesNotExist:
            return Response({'detail': 'Patient profile not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = PatientInfoSerializer(patient_profile)
    
        return Response( serializer.data, status=status.HTTP_200_OK)
    
    elif user.user_type == 'doctor':
        try:
            doctorProfile = DoctorProfile.objects.get(user=request.user)
        except doctorProfile.DoesNotExist:
            return Response({'detail': 'Doctor profile not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorInfoSerializer(doctorProfile)
    
        return Response( serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_list(request):
    patients = PatientProfile.objects.all()
    serializer = PatientInfoSerializer(patients, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def doctor_list(request):
    doctors = DoctorProfile.objects.all()
    serializer = DoctorInfoSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data

    user.email = data.get('email', user.email)
    user.username = data.get('username', user.username)

    if user.password != "":
        user.password = make_password(data.get('password', user.password))         
    user.save()

    try:
        if user.user_type == 'Patient':
            profile = user.user_patient
            profile.date_of_birth = data.get('date_of_birth', profile.date_of_birth)
            profile.chronic_diseases = data.get('chronic_diseases', profile.chronic_diseases)
            profile.x_ray = data.get('x_ray', profile.x_ray)
            profile.symptoms = data.get('symptoms', profile.symptoms)
            profile.save()
            serializer = PatientInfoSerializer(profile)

        elif user.user_type == 'Doctor':
            profile = user.user_doctor
            profile.img = data.get('img', profile.img)
            profile.master_degree = data.get('master_degree', profile.master_degree)
            profile.phd_degree = data.get('phd_degree', profile.phd_degree)
            profile.clink_location = data.get('clink_location', profile.clink_location)
            profile.medical_center = data.get('medical_center', profile.medical_center)
            profile.syndicate_card = data.get('syndicate_card', profile.syndicate_card)
            profile.save()
            serializer = DoctorInfoSerializer(profile)
        else:
            return Response({"detail": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

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
        "omar.moataz@gmail.com",
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
