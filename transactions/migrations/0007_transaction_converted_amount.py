# Generated by Django 3.0.6 on 2020-05-19 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_transaction_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='converted_amount',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=12),
        ),
    ]
