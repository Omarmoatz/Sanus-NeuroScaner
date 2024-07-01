from django.db import models

from accounts.models import CustomUser

class BrainPrediction(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user_prediction', on_delete=models.CASCADE)
    mri_img1 = models.ImageField( upload_to='mri_img', verbose_name='mri image', blank=True, null=True)
    mri_img2 = models.ImageField( upload_to='mri_img', verbose_name='mri image', blank=True, null=True)
    mri_img3 = models.ImageField( upload_to='mri_img', verbose_name='mri image', blank=True, null=True)
    prediction = models.CharField( max_length=900, blank=True, null=True)

    def __str__(self):
        return f'{str(self.user)} gets--> {self.prediction}'
