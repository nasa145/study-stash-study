# Generated by Django 4.2.6 on 2023-10-13 20:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('paymentapp', '0003_subscription_date_subscribeed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_subscribeed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
