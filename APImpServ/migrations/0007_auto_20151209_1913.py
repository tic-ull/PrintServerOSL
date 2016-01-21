# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APImpServ', '0006_print'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='print',
            name='printers',
        ),
        migrations.RemoveField(
            model_name='print',
            name='quotas',
        ),
        migrations.RemoveField(
            model_name='print',
            name='sessions',
        ),
        migrations.AlterModelOptions(
            name='printsession',
            options={'get_latest_by': 'date'},
        ),
        migrations.AlterField(
            model_name='quota',
            name='printer',
            field=models.ForeignKey(to='APImpServ.Printer'),
        ),
        migrations.DeleteModel(
            name='Print',
        ),
    ]
