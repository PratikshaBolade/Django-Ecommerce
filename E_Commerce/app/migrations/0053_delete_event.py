# Generated by Django 5.0.2 on 2024-04-15 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_rename_date_event_when'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
    ]
