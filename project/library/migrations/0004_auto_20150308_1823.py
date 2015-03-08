# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20150308_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='path',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='folder',
            name='path',
            field=models.CharField(default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='folder',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
