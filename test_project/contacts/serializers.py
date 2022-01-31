from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Contact model serializer.
    """
    
    class Meta:
        model = Contact
        fields = '__all__'