# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0009_auto_20171005_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservoir',
            name='actualHieght',
            field=models.FloatField(default=100),
        ),
    ]
