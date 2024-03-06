from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField( max_length=100,default='default_name')
    logo = models.ImageField( upload_to='company_logo')
    email_link = models.URLField( max_length=200, blank=True, null=True)
    whatsapp_link = models.URLField( max_length=200, blank=True, null=True)
    facebook_link = models.URLField( max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company info'
        verbose_name_plural = 'Company info'
class Article(models.Model):
    title = models.CharField( max_length=100,default='default_title')
    image = models.ImageField( upload_to='article_image')
    content = models.TextField( max_length=9000000, default='default_content')
    created_at = models.DateField( default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articls'
