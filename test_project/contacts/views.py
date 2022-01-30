from django.db.utils import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from .models import Contact
from django.shortcuts import get_object_or_404

class ContactViews(APIView):
    
    def get(self, request, phone_get=None):
        if phone_get:
            contact = get_object_or_404(Contact, phone_number=phone_get)
            serializer = ContactSerializer(contact)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        try:
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"status": "error", "data": 'This phone number already exist.'}, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, phone_patch):
        contact = get_object_or_404(Contact, phone_number=phone_patch)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})