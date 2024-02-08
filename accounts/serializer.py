from rest_framework import serializers
from django.contrib.auth.models import User

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        extra_kwargs = {
            'first_name':{'required':True},
            'last_name':{'required':True},
            'email':{'required':True},
            'password':{'required':True,'min_length':8}
        }

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']

