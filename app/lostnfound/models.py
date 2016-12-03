# Create your models here.
#Radhika Mattoo, @radhikamattoo, rm3485@nyu.edu
#Lost-n-Found Service
#Django Models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django import forms

class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Owner')
    #None means the owner has the item. True means someone has found the item and scanned the QR code. False means the item is lost and has not been found.
    qr_code = models.CharField('Code', max_length=1000)
    found = models.BooleanField('Found', default=None)
    name = models.CharField('Name', max_length=40)

    def __str__(self):
        return self.name + " owned by " + self.owner.first_name + " " + self.owner.last_name

#
# class UserForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=100)


class FinderForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    user_id = forms.CharField(widget=forms.HiddenInput)
    item_id = forms.CharField(widget=forms.HiddenInput)
