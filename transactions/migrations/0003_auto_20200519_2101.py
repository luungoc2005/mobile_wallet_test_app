# Generated by Django 3.0.6 on 2020-05-19 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200519_1855'),
        ('transactions', '0002_auto_20200519_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='from_account',
            field=models.ManyToManyField(related_name='transactions_to', to='accounts.Account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to_account',
            field=models.ManyToManyField(related_name='transactions_from', to='accounts.Account'),
        ),
    ]
