from datetime import datetime,timedelta
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .serializer import PatientInfoSerializer, DoctorInfoSerializer, SignUpSerializer, DoctorProfileSerializer 
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
            f"Welcome DR {username}.\n follow this link to activate your account --> {link}",
            "omar.moataz@gmail.com", # or use this to send yo gmail : settings.EMAIL_HOST_USER
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

    if not data or 'username' not in data or 'password' not in data:
        return Response({'error': 'please enter your username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

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
    
    else:
        return Response({"detail": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_list(request):
    try:
        doctor = request.user.user_doctor
    except ObjectDoesNotExist:
        return Response({'detail': 'No doctor profile found for this user'},
                        status=status.HTTP_404_NOT_FOUND)
    
    patients = PatientProfile.objects.filter(doctor=doctor).all()

    if not patients:
        return Response({'detail': 'No patients found for this doctor'},
                        status=status.HTTP_404_NOT_FOUND)
    
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

    if not data or 'email' not in data:
        return Response({'error': 'please enter your email'},
                         status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = get_object_or_404(CustomUser, email=data['email'])
    except CustomUser.DoesNotExist:
        return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
    
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)

    user.reset_password_token = token
    user.reset_password_expire_date = expire_date
    user.save()

    link = f"http://127.0.0.1:8000/accounts/reset_password/{token}/"

    send_mail(
        "Reset Password",
        f"Your Reset Password link : {link}",
        "omar.moataz@gmail.com", # or use this to send yo gmail : settings.EMAIL_HOST_USER
        [data['email']]
    )
    return Response({'detail':'sent the mail successfully'})




@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(CustomUser, reset_password_token = token)

    if not data or 'password' not in data or 'confirm_password' not in data:
        return Response({'error': 'please enter your password and confirm_password'},
                         status=status.HTTP_400_BAD_REQUEST)
    
    if len(data['password']) < 8 or len(data['confirm_password']) < 8:
        return Response({'error': 'password must be at least 8 characters'},
                         status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirm_password']:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.reset_password_expire_date is None or user.reset_password_expire_date.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'The token has expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.reset_password_token = ""
    user.reset_password_expire_date = None
    user.save()

    user.password = make_password(data['password'])
    user.save()

    return Response({'detail':'Reset the Password Successfully'})
