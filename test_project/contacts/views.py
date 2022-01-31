from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from .models import Contact
from django.shortcuts import get_object_or_404


class ContactViews(APIView):
    """
    API view for contact model.
    Available methods are GET, POST, PUT, DELETE.
    """
    # If phone_number is not provided it returns all contacts.
    def get(self, request, phone_number=None):
        if phone_number:
            contact = get_object_or_404(Contact, phone_number=phone_number)
            serializer = ContactSerializer(contact)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, phone_number=None):
        contact = Contact.objects.filter(phone_number=phone_number).first()
        if contact:
            serializer = ContactSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data})
            else:
                return Response({"status": "error", "data": serializer.errors})
        else:
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, phone_number=None):
        contact = get_object_or_404(Contact, phone_number=phone_number)
        contact.delete()
        return Response({"status": "success", "data": "Contact Deleted"})