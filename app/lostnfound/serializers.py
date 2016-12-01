'''
Provide a way of serializing and deserializing the <Models>
instances into representations such as json

We can do this by declaring serializers that work very similar to Django's forms.
'''


from rest_framework import serializers
## import all models to be serialized
