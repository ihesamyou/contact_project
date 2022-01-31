from django.test import TestCase, Client
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import status

c = Client()


class ContactModelTest(TestCase):
    """
    Contact model required fields and phone validation tests.
    """
    def setUp(self):
        self.user = Contact.objects.create(first_name='Testyahoo', phone_number='09137778899',
        last_name='family', email='ali@gmail.com', home='03135478899', work='03155544477', address='home address', emergency_contact=True,
        other='777888999111', notes='my note')
        self.test_user = Contact.objects.get(phone_number='09137778899')

    def test_required_fields(self):
        self.assertEqual(self.test_user.first_name, 'Testyahoo')
        self.assertEqual(self.test_user.phone_number, '09137778899')

    def test_phone_validation(self):
        self.user.phone_number = '0910'
        self.assertNotEqual(self.test_user.phone_number, '0913444111')

    def test_other_fields(self):
        self.assertEqual(self.user.last_name, 'family')
        self.assertEqual(self.user.email, 'ali@gmail.com')
        self.assertEqual(self.user.home, '03135478899')
        self.assertEqual(self.user.work, '03155544477')
        self.assertEqual(self.user.address, 'home address')
        self.assertEqual(self.user.emergency_contact, True)
        self.assertEqual(self.user.other, '777888999111')
        self.assertEqual(self.user.notes, 'my note')
        


class GetContactsTest(TestCase):
    """
    Test for API GET method.
    """
    def setUp(self):
        Contact.objects.create(
            first_name='Test4444', phone_number='09104445566')
        Contact.objects.create(
            first_name='Test5555', phone_number='09105556677')
        Contact.objects.create(
            first_name='Test6666', phone_number='09106667788')

    def test_get_all_contacts(self):
        response = c.get('')
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contact(self):
        response = c.get('/09104445566')
        contact = Contact.objects.get(phone_number='09104445566')
        serializer = ContactSerializer(contact)
        self.assertEqual(response.data['data'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test for get requests with a non existent contact.
    def test_get_invalid_contact(self):
        response = c.get('/09101111111')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class PostContactsTest(TestCase):
    """
    Test for API POST method.
    """
    def setUp(self):
        Contact.objects.create(
            first_name='Test4444', phone_number='09104445566')

    # test for post requests with a contact phone number that already exist in database.
    def test_post_invalid_contact(self):
        response = c.post('', {'phone_number': '09104445566', 'first_name': 'Test9999'}, content_type='application/json')
        contact = Contact.objects.get(phone_number='09104445566')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(contact.first_name, 'Test9999')

    # test for post requests with an invalid contact phone number.
    def test_post_invalid_phone_number(self):
        response = c.post('', {'phone_number': '0910', 'first_name': 'Test9999'}, content_type='application/json')
        contact = Contact.objects.filter(phone_number='09104445566').first()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(contact, None)
        
    def test_post_valid_contact(self):
        response = c.post('', {'phone_number': '09109999999', 'first_name': 'Test9999'}, content_type='application/json')
        contact = Contact.objects.get(phone_number='09109999999')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(contact.phone_number, '09109999999')
        self.assertEqual(contact.first_name, 'Test9999')
    


class PutContactsTest(TestCase):
    """
    Test for API PUT method.
    """
    def setUp(self):
        Contact.objects.create(
            first_name='Test4444', phone_number='09104445566')

    def test_put_existing_contact(self):
        response = c.put('/09104445566', {"phone_number": "09108887799", "first_name": "Test0000"}, content_type='application/json')
        contact = Contact.objects.get(phone_number='09108887799')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(contact.first_name, 'Test0000')

    def test_put_new_contact(self):
        response = c.put('', {"phone_number": "09109999999", "first_name": "Test9999"}, content_type='application/json')
        contact = Contact.objects.get(phone_number='09109999999')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(contact.first_name, 'Test9999')

    # test for put requests with an invalid phone number.
    def test_put_invalid_phone_number(self):
        response = c.put('', {"phone_number": "0910", "first_name": "Test9999"}, content_type='application/json')
        contact = Contact.objects.filter(phone_number='0910').first()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(contact, None)



class DeleteContactsTest(TestCase):
    """
    Test for API DELETE method.
    """
    def setUp(self):
        Contact.objects.create(
            first_name='Test4444', phone_number='09104445566')

    # test for deleting a non existent contact.
    def test_delete_invalid_contact(self):
        response = c.delete('/09101111111')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_contact(self):
        response = c.delete('/09104445566')
        contact = Contact.objects.filter(phone_number='09104445566').first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(contact, None)