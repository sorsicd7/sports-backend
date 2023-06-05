from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from ..models import Account

class AccountAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.account = Account.objects.create(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.account)

    def test_create_account(self):
        url = reverse('account:account-list-create')
        data = {
            'email': 'test2@example.com',
            'username': 'testuser2',
            'password': 'testpassword2',
            'first_name': 'Test2',
            'last_name': 'User2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Account.objects.last().email, 'test2@example.com')

    def test_get_account(self):
        url = reverse('account:account-detail', args=[self.account.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.account.email)

    def test_update_account(self):
        url = reverse('account:account-detail', args=[self.account.id])
        data = {
            'email': 'test3@example.com',
            'username': 'testuser3',
            'password': 'testpassword3',
            'first_name': 'Test3',
            'last_name': 'User3'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.email, 'test3@example.com')
        self.assertEqual(self.account.username, 'testuser3')

    def test_delete_account(self):
        url = reverse('account:account-detail', args=[self.account.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)