# Radhika Mattoo, rm3485@nyu.edu
# Large Scale Web Apps Fall 2016
# Views for lostnfound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from models import Item, FinderForm, MyUserCreationForm
from rest_framework import viewsets
from lostnfound.serializers import UserSerializer, ItemSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import sys

#Render the home page
def index(request):
    if request.user.is_authenticated():
        pk = str(request.user.pk)
        return HttpResponseRedirect('./users/' + pk + '/products')
    else:
        return anon_home(request)
def anon_home(request):
    return render(request, 'lostnfound/index.html', {})

#Render the login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            pk = str(user.pk)
            return HttpResponseRedirect('./users/' + pk + '/products')
        else:
            form = AuthenticationForm()
            return render(request, 'lostnfound/login.html', {'form': form, 'badLogin':True})
    else:
        form = AuthenticationForm()
        return render(request, 'lostnfound/login.html', {'form': form})

#Render the signup view
@csrf_exempt
def signup(request):
    # return HttpResponse("Hello! I'm still in the process of being implemented.")
    signup = MyUserCreationForm()
    return render(request, 'lostnfound/signup.html', {'form': signup})

#Handles a login

#Handles a signup!
@csrf_exempt
def authenticate_user(request):
    if request.method == 'POST':
        #get user data from post request
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=True)
            login(request, new_user)
        else:
            print form.errors
            raise Exception
        return render(request, 'lostnfound/items.html', {'user': new_user})
    else:
        form = MyUserCreationForm
        return render(request, 'lostnfound/signup.html', {'form': form})

#Handles GET & POST by a finder
@csrf_exempt
def handle_lost(request):
    if request.method == 'POST':
        finder = FinderForm(request.POST)
        if form.is_valid():
            finder_name = finder.name
            finder_email = finder.email
            user_id = finder.user_id
            item_id = finder.item_id
            item = Item.objects.get(pk=item_id, owner__pk=user_id) #TODO: Figure out how to handle filtering using a foreign key's primary key
            if item is not None:
                item.found = True
                item.save()
            return render(request, 'lostnfound/thankyou.html',{'item': item})
    else:
        item = Item.objects.get(pk=request.item)
        data = {
            'user_id': request.user,
            'item_id': request.item,
        }
        form = FinderForm(initial=data)
        return render(request, 'lostnfound/found.html', {'form':form, 'item': item})


# Authenticated views
#####################
#Retrieves and renders a list of a user's registered items, if any.
@login_required
def user_items(request, user_id):
    #Retrieve user from the request object
    try:
        my_user = User.objects.get(pk=user_id)
    except IndexError:
        raise Exception #yikes, there's no user!
    #Find all of user items
    my_items = Item.objects.filter(owner=my_user)
    context = {
        'user' : my_user,
        'items' : my_items
    }
    return render(request, 'lostnfound/items.html', context)


#Handles a GET and POST for registering an item
@login_required
def register_item(request):
    return HttpResponse("Hello! I'm still in the process of being implemented.")
    # if request.method == 'POST':
    #     #TODO: I need an ItemForm here!
    #     form = ItemForm(request.POST)
    #     new_item = form.save(commit=True) #Need to save the db object now in order to access its id.
    #     new_item.owner = request.user
    #     #Constructing URL for QR code
    #     url = 'http://myapp.com/users/' + request.user.pk + '/found/' + new_item.pk #FIXME: what's the hostname for our web app?
    #     new_item.qr_code = generate_qr(new_item.id) #TODO: I need the function call to generate the QR code!
    #     new_item.save()
    #     return print_qr_code(request, url, new_item.pk)
    # else:
    #     #TODO: I need an ItemForm here!
    #     form = ItemForm
    #     return render(request, 'lostnfound/register_item.html',{'form':form, 'user': request.user })

    #TODO: NEED TO REDIRECT TO A PAGE SO THE USER CAN PRINT THE QR CODE!

@login_required
def print_qr_code(request, url, new_item):
    return HttpResponse("Hello! I'm still in the process of being implemented.")
    #TODO: implement qr code generation embedded with the param url
    #render(request, 'lostnfound/qr_code.html', {PASS QR CODE IMG HERE, 'item': new_item})


#A user wants to delete an item.
@login_required
def delete_item(request):
    #delete the item based on the user and the primary key
    delete_item = Item.objects.get(pk=request.item) #TODO: Figure out how to handle filtering using a foreign key's primary key
    delete_item.delete()
    return user_items(request)

@login_required
def report_lost(request):
    return HttpResponse("Hello! I'm still in the process of being implemented.")
