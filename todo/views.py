# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todo
from .serializers import TodoSerializer


# Create your views here.
class TodoView(APIView):
    """
    TodoView used to handle the incoming requests relating to
    `todo` items
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        """
        Retrieve a complete list of `todo` items from the Todo
        model, serialize them to JSON and return the serialized
        todo items
        """
        if "username" in request.query_params:
            if pk is None:
                user = User.objects.get(username=request.query_params["username"])
                todo_items = Todo.objects.filter(user=user)
                serializer = TodoSerializer(todo_items, many=True)
                serialized_data = serializer.data
                return Response(serialized_data)
            else:
                todo = Todo.objects.get(id=pk)
                serializer = TodoSerializer(todo)
                serialized_data = serializer.data
                return Response(serialized_data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Handle the POST request for the `/todo/` endpoint.

        This view will take the `data` property from the `request` object,
        deserialize it into a `Todo` object and store in the DB.

        Returns a 201 (successfully created) if the item is successfully
        created, otherwise returns a 400 (bad request)
        """

        serializer = TodoSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(username=request.data["username"])
            data = serializer.data
            Todo.objects.create(user=user, title=data["title"],
                                description=data["description"],
                                status=data["status"])
            
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """
        Handle PUT request for the `/todo/` endpoint.

        Retrieves a `todo` instance based on the primary key contained
        in the URL. Then takes the `data` property from the `request` object
        to update the relevant `todo` instance.

        Returns the updated object if the update was successful, otherwise
        400 (bad request) is returned
        """
        todo = Todo.objects.get(id=pk)
        serializer = TodoSerializer(todo, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        """
        Handle DELETE request for the `/todo/` endpoint.

        Retrieves a `todo` instance based on the primary key contained
        in the URL and then deletes the relevant instance.

        Returns a 204 (no content) status to indicate that the item was deleted.
        """
        todo = Todo.objects.get(id=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
