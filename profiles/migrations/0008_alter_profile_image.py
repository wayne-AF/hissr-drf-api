# Generated by Django 3.2.18 on 2023-04-09 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_profile_seeking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='../default_profile_pic_2_a59qhb', upload_to='images/'),
        ),
    ]