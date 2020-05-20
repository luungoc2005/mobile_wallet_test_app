from django.shortcuts import render
from django.db.models import F, Q, ObjectDoesNotExist
# Create your views here.
from transactions.models import Transaction
from accounts.models import Account
from django.utils.translation import gettext_lazy as _
from rest_framework import routers, serializers, viewsets, views, permissions, exceptions

import requests

class AccountField(serializers.RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected pk value, received {data_type}.'),
    }

    def __init__(self, **kwargs):
        self.queryset = Account.objects.all().only('currency', 'balance', 'owner')
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.queryset.get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return str(value)


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    from_account = AccountField()
    to_account = AccountField()

    class Meta:
        model = Transaction
        fields = ['id', 'from_account', 'to_account', 'amount', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        from_instance = validated_data.pop('from_account')
        to_instance = validated_data.pop('to_account')
        amount = validated_data.pop('amount')

        if from_instance == to_instance:
            raise ValueError("Source and target accounts are the same")

        converted_amount = amount

        if from_instance.owner != self.context["request"].user:
            raise exceptions.PermissionDenied()

        if amount > from_instance.balance:
            raise exceptions.NotAcceptable("Insufficient balance")

        if from_instance.currency != to_instance.currency:
            currency = to_instance.currency.upper()

            r = requests.get(f'https://api.exchangeratesapi.io/latest?base={from_instance.currency}')
            rates_data = r.json()["rates"]

            if currency not in rates_data:
                raise exceptions.NotAcceptable("Currency not supported")

            converted_amount /= Decimal(rates_data[currency])

        from_instance.balance = F('balance') - amount
        to_instance.balance = F('balance') + converted_amount

        transaction = Transaction.objects.create(
            from_account=from_instance, 
            to_account=to_instance, 
            amount=amount,
            converted_amount=converted_amount
        )
        from_instance.save()
        to_instance.save()

        return transaction


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    http_method_names = ['get', 'post']
    ordering = ['-created_at']

    def get_serializer_context(self):
        context = super(TransactionViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return Transaction.objects.filter(
            Q(from_account__owner=self.request.user) | Q(to_account__owner=self.request.user)
        )