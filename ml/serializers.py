from rest_framework import serializers
from .models import Image, Prediction

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']

class MultipleImageSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField()
    )