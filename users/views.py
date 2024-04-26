from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LogInSerializer


# Create your views here.
class RegistrationView(viewsets.ViewSet):
    serializer_class = RegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)


class LogInView(viewsets.ViewSet):
    serializer_class = LogInSerializer

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=data["email"], password=data["password"])
        if user is None:
            return Response({"Error": "Incorrect email or password"}, 401)
        return Response({"UID": user.id}, 200)
