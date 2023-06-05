# Generated by Django 4.1 on 2023-06-05 13:18

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230605_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[accounts.models.validate_phone_number], verbose_name='=شماره تماس'),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='نام کاربری'),
        ),
    ]