# Create your models here.
#Radhika Mattoo, @radhikamattoo, rm3485@nyu.edu
#Mohammad Afshar, @mafshar, ma2510@nyu.edu
#Lost-n-Found Service
#Django Models
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django import forms

class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Owner')
    #None means the owner has the item. True means someone has found the item and scanned the QR code. False means the item is lost and has not been found.
    qr_code = models.CharField('Code', max_length=1000)
    found = models.NullBooleanField('Found')
    name = models.CharField('Name', max_length=40)

    def __str__(self):
        return self.name + " owned by " + self.owner.first_name

class FinderForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    user_id = forms.CharField(widget=forms.HiddenInput)
    item_id = forms.CharField(widget=forms.HiddenInput)

class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=commit)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
