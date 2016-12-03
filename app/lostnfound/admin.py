from django.contrib import admin

#below subject to change based on change to models.py
from lostnfound.models import User, Item

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
