# Generated by Django 5.0.4 on 2024-04-29 23:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0009_alter_businesslist_count_num_alter_businesslist_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesslist',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 29, 17, 25, 26, 610222)),
        ),
    ]
