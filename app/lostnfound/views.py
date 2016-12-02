from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import loader
from models import Item
from rest_framework import viewsets
from lostnfound.serializers import UserSerializer, ItemSerializer

# Create your views here.
from django.http import HttpResponse

def signup(request):
    template = loader.get_template('lostnfound/index.html')
    context = {}
    return HttpResponse(template.render(context,request))

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
