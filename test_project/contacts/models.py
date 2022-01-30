from django.db import models
from django.core.validators import RegexValidator


class Contact(models.Model):
    """
    Contact model for saving contacts information.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    # For phone numbers, CharField is used to avoid having any problem in case of
    # having a number starting with 0. we validate phone number with phone_regex.
    # other numbers are are not validated because of their complexity.
    phone_regex = RegexValidator(regex=r'(\+/d/d)?\d{10,11}', message='Phone number should be like one of theses formats: +989135556677 or 09135556677')
    phone_number = models.CharField(unique=True, verbose_name='Phone', validators=[phone_regex])
    home = models.CharField(blank=True, null=True, max_length=16)
    work = models.CharField(blank=True, null=True, max_length=16)
    email = models.EmailField(unique=True, blank=True, null=True)
    other = models.CharField(blank=True, null=True, verbose_name='other numbers', max_length=16)
    address = models.CharField(blank=True, null=True, max_length=300)
    emergency_contact = models.BooleanField(default=False, help_text='Call this contact in case of emergency.')
    notes = models.TextField(blank=True, null=True)