# Generated by Django 5.0.2 on 2024-03-06 13:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aboutUs', '0002_alter_article_options_alter_company_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='email_link',
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='company',
            name='facebook_link',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='whatsapp_link',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
