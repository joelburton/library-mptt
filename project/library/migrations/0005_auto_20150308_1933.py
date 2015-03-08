# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20150308_1823'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set([('slug', 'folder'), ('title', 'folder')]),
        ),
    ]
