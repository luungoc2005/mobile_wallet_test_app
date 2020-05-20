from django.test import TestCase
from accounts.models import Account
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import json

class AccountsModelTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', password='secret')
        self.user = User.objects.create_user('testuser', 'test@test.com', password='secret')

        self.admin_acc_1 = Account.objects.create(owner=self.superuser)
        self.user_acc_1 = Account.objects.create(owner=self.user)
        self.user_acc_2 = Account.objects.create(owner=self.user)

        self.user_client = APIClient()
        self.user_client.login(username='testuser', password='secret')

        self.admin_client = APIClient()
        self.admin_client.login(username='admin', password='secret')

    def test_user_can_list_own_accounts(self):
        response = self.user_client.get('/accounts', format='json', follow=True)
        response = response.json()
        self.assertEqual(len(response["results"]), 2)

    def test_admin_can_list_own_accounts(self):
        response = self.admin_client.get('/accounts', format='json', follow=True)
        response = response.json()
        self.assertEqual(len(response["results"]), 1)

    def test_admin_can_deposit_funds(self):
        account_id = str(self.user_acc_1.id)
        response = self.admin_client.post('/deposit/', {
            "account_id": account_id,
            "amount": 20
        }, format='json', follow=True)
        self.user_acc_1.refresh_from_db()
        self.assertEqual(self.user_acc_1.balance, 20)
