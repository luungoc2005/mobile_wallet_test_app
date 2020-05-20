from django.shortcuts import render
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

# Create your views here.
from accounts.models import Account
from rest_framework import routers, serializers, viewsets, permissions, exceptions
from decimal import Decimal

import requests
import uuid

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.owner == request.user:
            return True

        return request.user.is_staff


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'currency', 'balance', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
        }
    
    def create(self, validated_data):
        validated_data.pop('balance')
        return super(AccountSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        currency = validated_data.get('currency')
        balance = validated_data.get('balance', instance.balance)

        return super(AccountSerializer, self).update(instance, {'balance': balance})


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'put']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.request.method in ['POST', 'PUT']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated(), IsOwnerOrAdmin()]

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user) \
            .only('id', 'currency', 'balance')


class DepositSerializer(serializers.Serializer):
    account_id = serializers.UUIDField(allow_null=False)
    amount = serializers.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=5,
        allow_null=False
    )
    currency = serializers.CharField(max_length=5, allow_null=True, default=None)

class DepositViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['post']

    def create(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            account_id = validated_data.get('account_id')
            amount = validated_data.get('amount', 0)
            currency = validated_data.get('currency', None)

            account = Account.objects.only('id', 'balance', 'currency').get(id=account_id)

            if currency is not None and account.currency != currency:
                currency = currency.upper()

                r = requests.get(f'https://api.exchangeratesapi.io/latest?base={account.currency}')
                rates_data = r.json()["rates"]

                if currency not in rates_data:
                    raise ValueError("Currency not supported")
            
                amount /= Decimal(rates_data[currency])

            account.balance = F('balance') + amount
            account.save()

            return Response({
                'id': account_id,
                'amount': amount
            })