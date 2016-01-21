# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APImpServ', '0005_auto_20151202_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Print',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('printers', models.ForeignKey(to='APImpServ.Printer')),
                ('quotas', models.ForeignKey(to='APImpServ.UserQuota')),
                ('sessions', models.ForeignKey(to='APImpServ.PrintSession')),
            ],
        ),
    ]
