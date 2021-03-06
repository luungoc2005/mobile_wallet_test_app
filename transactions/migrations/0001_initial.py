# Generated by Django 3.0.6 on 2020-05-20 12:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=5, default=0, max_digits=12)),
                ('converted_amount', models.DecimalField(decimal_places=5, default=0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfers', to='accounts.Account')),
                ('to_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deposits', to='accounts.Account')),
            ],
        ),
    ]
