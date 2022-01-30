from django.test import TestCase
from .models import Contact

class ContactModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Contact.objects.create(first_name='Test', phone_number='09137778899')

    def test_required_fields(self):
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.phone_number, '09137778899')

    def test_phone_validation(self):
        self.user.phone_number=='0913444111'
        self.assertNotEqual(self.user.phone_number, '0913444111')
        