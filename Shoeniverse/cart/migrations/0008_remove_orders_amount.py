# Generated by Django 4.0 on 2022-02-10 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='amount',
        ),
    ]
