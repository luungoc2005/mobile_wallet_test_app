"""mobile_wallet_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.contrib.auth.models import User
from django.db.models import Sum
from accounts.models import Account
from accounts.views import AccountViewSet, DepositViewSet
from transactions.views import TransactionViewSet
from rest_framework import routers, serializers, viewsets, permissions

class UserSerializer(serializers.HyperlinkedModelSerializer):
    accounts = serializers.StringRelatedField(
        many=True, 
        read_only=True,
    )
    balance = serializers.SerializerMethodField('calculate_balance')

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'accounts', 'password', 'balance']
        extra_kwargs = {
            'password': {'write_only': True},
        }
   
    def calculate_balance(self, instance):
        request = self.context.get('request')
        user = request.user
        q = Account.objects.filter(owner=instance).aggregate(Sum('balance'))
        return list(q.values())[0]

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering = ['username']

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'deposit', DepositViewSet, basename='deposit')
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
]
