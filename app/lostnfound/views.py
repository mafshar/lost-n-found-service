from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from lostnfound.serializers import UserSerializer, ItemSerializer


# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the lost-n-found base.")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
