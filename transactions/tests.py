from django.test import TestCase
from accounts.models import Account
from transactions.models import Transaction
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class TransactionsModelTestCase(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', password='secret')
        self.user = User.objects.create_user('testuser', 'test@test.com', password='secret')

        self.admin_acc_1 = Account.objects.create(owner=self.superuser, balance=20)
        self.user_acc_1 = Account.objects.create(owner=self.user, balance=20)
        self.user_acc_2 = Account.objects.create(owner=self.user)

        self.user_client = APIClient()
        self.user_client.login(username='testuser', password='secret')

        self.admin_client = APIClient()
        self.admin_client.login(username='admin', password='secret')

    def test_user_can_create_transaction(self):
        orig_balance_1 = self.user_acc_1.balance
        orig_balance_2 = self.user_acc_2.balance
        amount = 10

        response = self.user_client.post('/transactions/', {
            'from_account': str(self.user_acc_1.id),
            'to_account': str(self.user_acc_2.id),
            'amount': amount
        }, format='json', follow=True)
        
        # transaction created
        queryset = Transaction.objects.filter(
            from_account=self.user_acc_1,
            to_account=self.user_acc_2
        )
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].amount, 10)

        self.user_acc_1.refresh_from_db()
        self.user_acc_2.refresh_from_db()

        self.assertEqual(self.user_acc_1.balance, orig_balance_1 - amount)
        self.assertEqual(self.user_acc_2.balance, orig_balance_2 + amount)