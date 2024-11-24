# Generated by Django 5.1.3 on 2024-11-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_app', '0002_customuser_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(default='default.png', null=True, upload_to='profile_pictures/%y/%m/%d/'),
        ),
    ]
