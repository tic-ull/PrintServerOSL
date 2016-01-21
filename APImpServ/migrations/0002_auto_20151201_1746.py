# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APImpServ', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userquota',
            old_name='mes',
            new_name='month',
        ),
        migrations.RenameField(
            model_name='userquota',
            old_name='año',
            new_name='year',
        ),
    ]
