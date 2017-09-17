# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer

# Create your views here.
class UserView(APIView):
    permission_classes = ()

    def post(self, request):
        """
        Handles the POST request made to the `/accounts/` URL.

        This view will take the `data` property from the `request` object,
        deserialize it into a `User` object and store in the DB.

        Returns a 201 (successfully created) if the user is successfully
        created, otherwise returns a 400 (bad request)
        """
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            user = User.objects.create(username=data["username"])
            user.set_password(data["password"])
            user.save()
            return Response(data, status=status.HTTP_201_CREATED)
