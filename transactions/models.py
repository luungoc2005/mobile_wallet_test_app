from django.db import models
from accounts.models import Account
import uuid

# Create your models here.

class Transaction(models.Model):
    id = models.UUIDField( 
            primary_key=True, 
            default=uuid.uuid4, 
            editable=False,
            null=False
        )
    from_account = models.ForeignKey(
            Account,
            related_name='transfers',
            on_delete=models.SET_NULL,
            null=True
        )
    to_account = models.ForeignKey(
            Account,
            related_name='deposits',
            on_delete=models.SET_NULL,
            null=True
        )
    amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=5,
        null=False
    )
    converted_amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=5,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.amount}"