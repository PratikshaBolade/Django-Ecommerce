# Generated by Django 5.0.2 on 2024-04-06 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_remove_order_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
