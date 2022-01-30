from django.test import TestCase
from .models import Contact

class ContactModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Contact.objects.create(first_name='Testyahoo', phone_number='09137778899')
        cls.test_user = Contact.objects.get(phone_number='09137778899')

    def test_required_fields(self):
        self.assertEqual(self.test_user.first_name, 'Testyahoo')
        self.assertEqual(self.test_user.phone_number, '09137778899')

    def test_phone_validation(self):
        self.user.phone_number = '0913444111'
        self.assertNotEqual(self.test_user.phone_number, '0913444111')
        