# Generated by Django 3.2.18 on 2023-03-30 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='../hissr_profile_default_ftjipg', upload_to='images/'),
        ),
    ]
