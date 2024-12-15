from rest_framework import viewsets
from .models import UserModel
from rest_framework import permissions
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        users = UserModel.objects.all()
        seralizer = UserSerializer(users, many=True)
        return Response(seralizer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs.get("pk"))
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs.get("pk"))
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs.get("pk"))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=kwargs.get("pk"))
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)