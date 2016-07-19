# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='licence',
            field=models.CharField(max_length=255, null=True, choices=[(b'cc-by', b'CC-BY'), (b'cc-by-sa', b'CC-BY-SA'), (b'cc-by-nc', b'CC-BY-NC'), (b'cc-by-nc-sa', b'CC-BY-NC-SA'), (b'cc-by-nd', b'CC-BY-ND'), (b'cc-by-nc-nd', b'CC-BY-NC-ND'), (b'cc0', b'Public Domain (CC0)'), (b'free-art', b'Free Art Licence'), (b'wtfpl', b'WTFpl'), (b'other', b'Other (put it in the description)')]),
        ),
    ]
