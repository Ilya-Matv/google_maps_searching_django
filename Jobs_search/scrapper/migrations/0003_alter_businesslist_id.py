# Generated by Django 5.0.4 on 2024-04-16 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0002_remove_businesslist_businesses_alter_businesslist_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesslist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
