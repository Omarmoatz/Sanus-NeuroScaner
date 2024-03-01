from rest_framework import serializers
from django.contrib.auth.models import User

class SignUpSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username','email','password','password_confirmation']
        extra_kwargs = {
            'username':{'required':True},
            'email':{'required':True},
            'password':{'required':True,'min_length':8},
            'password_confirmation':{'required':True,'min_length':8},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        return super().create(validated_data)
    
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username']

