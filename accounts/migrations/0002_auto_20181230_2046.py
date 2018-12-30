# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-12-30 20:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=b'documents/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='short_bio',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]