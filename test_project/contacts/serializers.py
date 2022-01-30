from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Contact model serializer.
    Only phone number is required.
    """
    first_name = serializers.CharField(required=False, max_length=100)
    last_name = serializers.CharField(required=False, max_length=100)
    phone_number = serializers.CharField(max_length=11)
    home = serializers.CharField(required=False, max_length=16)
    work = serializers.CharField(required=False, max_length=16)
    email = serializers.EmailField(required=False)
    other = serializers.CharField(required=False, max_length=16)
    address = serializers.CharField(required=False, max_length=300)
    emergency_contact = serializers.BooleanField(required=False)
    notes = serializers.CharField(required=False)

    class Meta:
        model = Contact
        fields = ('__all__')