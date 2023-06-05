from django.test import TestCase
from rest_framework.exceptions import ValidationError
from ..models import Account
from ..serializers import AccountSerializer

class AccountSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
            'is_trainer': False,
            'is_student': True,
            'phone_number': '09901114111',
            'description': 'Test description',
        }
        self.serializer = AccountSerializer()
    
    def test_valid_data(self):
        serializer = AccountSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        account = serializer.save()
        self.assertEqual(account.email, self.valid_data['email'])
        self.assertEqual(account.username, self.valid_data['username'])
        self.assertEqual(account.first_name, self.valid_data['first_name'])
        self.assertEqual(account.last_name, self.valid_data['last_name'])
        self.assertTrue(account.check_password(self.valid_data['password']))
        self.assertEqual(account.is_trainer, self.valid_data['is_trainer'])
        self.assertEqual(account.is_student, self.valid_data['is_student'])
        self.assertEqual(account.phone_number, self.valid_data['phone_number'])
        self.assertEqual(account.description, self.valid_data['description'])
    
    def test_missing_required_fields(self):
        # Test that required fields are validated
        invalid_data = self.valid_data.copy()
        del invalid_data['email']
        del invalid_data['username']
        serializer = AccountSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('username', serializer.errors)
        
    def test_password_min_length(self):
        # Test that password length is validated
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = 'short'
        serializer = AccountSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
    
    def test_create_user(self):
        # Test that create() method creates a new user
        serializer = AccountSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        account = serializer.create(serializer.validated_data)
        self.assertIsInstance(account, Account)
        
    def test_update_user(self):
        # Test that update() method updates an existing user
        account = Account.objects.create_user(**self.valid_data)
        updated_data = self.valid_data.copy()
        updated_data['first_name'] = 'Updated'
        serializer = AccountSerializer(instance=account, data=updated_data)
        serializer.is_valid(raise_exception=True)
        updated_account = serializer.update(account, serializer.validated_data)
        self.assertEqual(updated_account.first_name, updated_data['first_name'])
        self.assertTrue(updated_account.check_password(self.valid_data['password']))
        
    def test_update_password(self):
        # Test that update() method updates password if password field is present
        account = Account.objects.create_user(**self.valid_data)
        updated_data = self.valid_data.copy()
        updated_data['password'] = 'newpassword'
        serializer = AccountSerializer(instance=account, data=updated_data)
        serializer.is_valid(raise_exception=True)
        updated_account = serializer.update(account, serializer.validated_data)
        self.assertTrue(updated_account.check_password(updated_data['password']))