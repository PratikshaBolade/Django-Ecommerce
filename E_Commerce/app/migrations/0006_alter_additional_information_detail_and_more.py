# Generated by Django 5.0.2 on 2024-02-16 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_additional_information_specification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additional_information',
            name='detail',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='additional_information',
            name='specification',
            field=models.CharField(max_length=100),
        ),
    ]
