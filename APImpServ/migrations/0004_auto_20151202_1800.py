# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APImpServ', '0003_auto_20151202_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquota',
            name='user',
            field=models.ForeignKey(to='APImpServ.UserProfile'),
        ),
    ]
