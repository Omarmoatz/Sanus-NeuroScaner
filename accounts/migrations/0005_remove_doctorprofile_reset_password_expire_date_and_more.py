# Generated by Django 5.0.2 on 2024-06-06 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_managers_alter_customuser_user_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorprofile',
            name='reset_password_expire_date',
        ),
        migrations.RemoveField(
            model_name='doctorprofile',
            name='reset_password_token',
        ),
        migrations.RemoveField(
            model_name='patientprofile',
            name='reset_password_expire_date',
        ),
        migrations.RemoveField(
            model_name='patientprofile',
            name='reset_password_token',
        ),
        migrations.AddField(
            model_name='customuser',
            name='reset_password_expire_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='reset_password_token',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
