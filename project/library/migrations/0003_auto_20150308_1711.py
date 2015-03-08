# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='folder',
            field=mptt.fields.TreeForeignKey(related_name='documents', to='library.Folder'),
        ),
    ]
