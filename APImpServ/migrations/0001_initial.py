# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicUser',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, parent_link=True, to=settings.AUTH_USER_MODEL, serialize=False, auto_created=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, serialize=False, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('n_pages', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('uri', models.URLField()),
                ('color', models.BooleanField(default=False)),
                ('paper_size', models.CharField(max_length=5)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, serialize=False, primary_key=True)),
                ('quota', models.CharField(max_length=4)),
                ('printer', models.OneToOneField(to='APImpServ.Printer')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuota',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, serialize=False, primary_key=True)),
                ('quota', models.CharField(max_length=4)),
                ('mes', models.CharField(default=12, max_length=2)),
                ('año', models.CharField(default=2015, max_length=4)),
                ('printer', models.ForeignKey(to='APImpServ.Printer', related_name='printers')),
                ('user', models.OneToOneField(to='APImpServ.BasicUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.UUIDField(editable=False, default=uuid.uuid4, serialize=False, primary_key=True)),
                ('type_name', models.CharField(max_length=50)),
                ('default', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='quota',
            name='user_type',
            field=models.ForeignKey(to='APImpServ.UserType', related_name='Quotas'),
        ),
        migrations.AddField(
            model_name='logs',
            name='printer',
            field=models.ForeignKey(to='APImpServ.Printer'),
        ),
        migrations.AddField(
            model_name='logs',
            name='user',
            field=models.ForeignKey(to='APImpServ.BasicUser'),
        ),
        migrations.AddField(
            model_name='basicuser',
            name='user_type',
            field=models.ForeignKey(to='APImpServ.UserType', related_name='users'),
        ),
    ]
