# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('APImpServ', '0002_auto_20151201_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.UUIDField(primary_key=True, editable=False, serialize=False, default=uuid.uuid4)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('user_type', models.ForeignKey(to='APImpServ.UserType', related_name='users')),
            ],
        ),
        migrations.RemoveField(
            model_name='basicuser',
            name='user_ptr',
        ),
        migrations.RemoveField(
            model_name='basicuser',
            name='user_type',
        ),
        migrations.AlterField(
            model_name='logs',
            name='user',
            field=models.ForeignKey(to='APImpServ.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userquota',
            name='user',
            field=models.OneToOneField(to='APImpServ.UserProfile'),
        ),
        migrations.DeleteModel(
            name='BasicUser',
        ),
    ]
