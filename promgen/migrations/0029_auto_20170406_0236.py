# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 02:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promgen', '0028_url_sort_fields'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rule',
            options={'ordering': ['service', 'name']},
        ),
        migrations.AlterField(
            model_name='rule',
            name='name',
            field=models.CharField(max_length=128, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z_]*$', 'Only alphanumeric characters are allowed.')]),
        ),
    ]
