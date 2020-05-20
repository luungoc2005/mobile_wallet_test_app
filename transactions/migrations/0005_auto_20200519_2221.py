# Generated by Django 3.0.6 on 2020-05-19 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200519_2209'),
        ('transactions', '0004_auto_20200519_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='from_account',
        ),
        migrations.AddField(
            model_name='transaction',
            name='from_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfers', to='accounts.Account'),
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='to_account',
        ),
        migrations.AddField(
            model_name='transaction',
            name='to_account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deposits', to='accounts.Account'),
        ),
    ]
