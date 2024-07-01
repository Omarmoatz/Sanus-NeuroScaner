from django.db import models

from accounts.models import CustomUser

class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='MRIimages/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Prediction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.user)} gets--> {self.result}'
