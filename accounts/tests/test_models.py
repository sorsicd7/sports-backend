from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Account, validate_phone_number

class AccountModelTest(TestCase):
    def setUp(self):
        # Create a test account
        self.account = Account(email='test@example.com', username='testuser', password = "testpassword")
        self.account.save()

    def test_phone_number_validation(self):
        # Test valid phone number
        valid_phone_number = '09123456789'
        validate_phone_number(valid_phone_number)  # should not raise ValidationError

        # Test invalid phone number
        invalid_phone_number = '12345678901'
        with self.assertRaises(ValidationError) as cm:
            validate_phone_number(invalid_phone_number)
        self.assertEqual(cm.exception.message, 'phone number is not valid')
        def test_str_representation(self):
            # Test that the account's email is returned as a string representation
            self.assertEqual(str(self.account), 'test@example.com')

    def test_is_staff_property(self):
        # Test that the is_staff property returns the correct value
        self.assertFalse(self.account.is_staff)  # should be False by default

        self.account.is_admin = True
        self.assertTrue(self.account.is_staff)  # should be True if is_admin is True

    def test_required_fields(self):
        # Test that the required fields are set correctly
        self.assertEqual(Account._meta.get_field('email').blank, False)
        self.assertEqual(Account._meta.get_field('email').null, False)
        self.assertEqual(Account._meta.get_field('username').blank, False)
        self.assertEqual(Account._meta.get_field('username').null, False)

    def test_username_uniqueness(self):
        # Test that the username field is unique
        with self.assertRaises(ValidationError) as cm:
            account3 = Account(email='test3@example.com', username='testuser', password='testpassword3')
            account3.full_clean()
            account3.save()

