#Radhika Mattoo, @radhikamattoo, rm3485@nyu.edu
#Lost-n-Found Service
#Django Models

from django.db import models
from django.contrib.auth.models import User



class Item(models.model):
    owner = models.ForeignKey('Owner', User)
    code = models.CharField('Code')
    name = models.CharField('Name', max_length=40)
