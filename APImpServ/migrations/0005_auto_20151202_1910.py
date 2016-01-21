# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('APImpServ', '0004_auto_20151202_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintSession',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('session', models.UUIDField(editable=False, default=uuid.uuid4)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to='APImpServ.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='printer',
            name='network',
            field=models.CharField(default='0.0.0.0/24', max_length=20),
        ),
    ]
