# Generated by Django 3.1 on 2020-08-18 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='id',
        ),
        migrations.AlterField(
            model_name='orders',
            name='paymentCode',
            field=models.CharField(max_length=400, primary_key=True, serialize=False),
        ),
    ]
