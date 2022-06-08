# Generated by Django 4.0.4 on 2022-06-06 14:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0013_profile_blockedusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='blockedUsers',
            field=models.ManyToManyField(blank=True, related_name='blockedUsers', to=settings.AUTH_USER_MODEL),
        ),
    ]