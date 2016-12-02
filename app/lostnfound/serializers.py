'''
Provide a way of serializing and deserializing the <Models>
instances into representations such as json

We can do this by declaring serializers that work very similar to Django's forms.
'''

## import all models to be serialized
from rest_framework import serializers
from django.contrib.auth.models import User
from models import Item
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('owner', 'found', 'qr_code', 'name')
