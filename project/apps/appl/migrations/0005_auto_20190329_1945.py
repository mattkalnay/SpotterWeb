# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-29 19:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appl', '0004_auto_20190329_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='Message',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='Image',
            new_name='message_image',
        ),
    ]
