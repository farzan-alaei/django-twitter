# Generated by Django 5.0.2 on 2024-03-07 16:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userfollowing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='userfollowing',
            name='following_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p', to=settings.AUTH_USER_MODEL, verbose_name='followers'),
        ),
    ]
