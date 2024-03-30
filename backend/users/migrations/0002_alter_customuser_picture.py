# Generated by Django 5.0.3 on 2024-03-30 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='picture',
            field=models.FileField(blank=True, default='profile_picture.jpg', null=True, upload_to='profile_pictures/', verbose_name='Profile Picture'),
        ),
    ]
