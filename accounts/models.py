from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.


class Account(models.Model):
    id = models.UUIDField( 
            primary_key=True, 
            default=uuid.uuid4, 
            editable=False,
            null=False
        )
    owner = models.ForeignKey(
            User,
            related_name='accounts',
            on_delete=models.SET_NULL,
            null=True
        )
    currency = models.CharField(max_length=5, default='SGD', null=False)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=5,
        null=False
    )
    is_archived = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} ({self.currency})"