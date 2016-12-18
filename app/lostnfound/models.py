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
from django.forms import ModelForm

class Item(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Owner')
    qr_code = models.CharField(default=None, max_length=800, null=True)
    #None means the owner has the item. True means someone has found the item and scanned the QR code. False means the item is lost and has not been found.
    found = models.NullBooleanField('Found', default=None)
    name = models.CharField('Name', max_length=40)

    def __str__(self):
        return self.name

class FinderForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    user_id = forms.CharField(widget=forms.HiddenInput)
    item_id = forms.CharField(widget=forms.HiddenInput)

class ItemForm(ModelForm):
    name = forms.CharField(max_length=50, required=True)
    class Meta:
        model = Item
        fields = ("name",)
        exclude = ("owner","qr_code")


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

    def email_user(self, finder_email):
        '''
        Sends an email to this User.
        '''
        sender = 'noreply.itemfound@gmail.com'
        if finder_email:
            try:
                send_mail(
                    'Your item has been found!',
                    'Someone has found your lost item! This message will facilitate your item\'s return.',
                    sender,
                    [self.cleaned_data["email"], finder_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')
        
