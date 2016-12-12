# Radhika Mattoo, rm3485@nyu.edu
# Large Scale Web Apps Fall 2016
# Views for lostnfound

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from models import Item, FinderForm, ItemForm, MyUserCreationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.conf import settings
import sys
from qrcode import *

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
    if request.user.is_authenticated():
        pk = str(request.user.pk)
        return HttpResponseRedirect('./users/' + pk + '/products')
    form = AuthenticationForm()
    return render(request, 'lostnfound/login.html', {'form': form})

#Render the signup view
def signup(request):
    if request.user.is_authenticated():
        pk = str(request.user.pk)
        return HttpResponseRedirect('./users/' + pk + '/products')
    else:
        signup = MyUserCreationForm()
        return render(request, 'lostnfound/signup.html', {'form': signup})

#Handles a signup
def authenticate_user(request):
    if request.method == 'POST':
        if 'signup' in request.POST: #signup
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=True)
                login(request, new_user)
                pk = str(new_user.pk)
                return HttpResponseRedirect('./users/' + pk + '/products')
            else:
                return render(request, 'lostnfound/signup.html', {'form': form})
        else: #login
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
        return HttpResponseRedirect('./')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('lostnfound/logged_out.html')

#Handles GET & POST by a finder
def handle_lost(request, user_id, product_id):
    if request.method == 'POST':
        finder = FinderForm(request.POST)
        if finder.is_valid():
            finder_name = finder.data['name']
            finder_email = finder.data['email']
            user_id = finder.data['user_id']
            item_id = finder.data['item_id']
            item = Item.objects.get(pk=item_id, owner__pk=user_id)
            if item is not None:
                item.found = True
                item.save()
            return render(request, 'lostnfound/thankyou.html',{'item': item})
    else:
        item = Item.objects.get(pk=product_id)
        user = User.objects.get(pk=user_id)
        data = {
            'user_id': user_id,
            'item_id': product_id,
        }
        form = FinderForm(initial=data)
        return render(request, 'lostnfound/found.html', {'form':form, 'item': str(item), 'user': user.first_name})


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
    show_form = False
    for item in my_items:
        if item.found is None:
            show_form = True
    context = {
        'user' : my_user,
        'items' : my_items,
        'show_form' : show_form
    }
    return render(request, 'lostnfound/items.html', context)

#function to generate unique item id that includes user id in the first part
def generate_item_id(user):
    user_id = user.pk
    user_items = Item.objects.filter(owner__pk=user_id)
    num_of_items = len(user_items) + 1
    item_id = int(str(user_id) + str(num_of_items))

    return item_id

#Handles a GET and POST for registering an item
@login_required
def register_item(request, user_id):
    my_user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        new_item = form.save(commit=False)
        new_item.owner = my_user
        new_item.save()
        return HttpResponseRedirect("/users/" + user_id + "/products/" + str(new_item.pk))
    else:
        form = ItemForm()
        return render(request, 'lostnfound/register_item.html',{'form':form, 'user': my_user })

@login_required
def print_qr_code(request, user_id, product_id):
    item = Item.objects.get(pk=product_id)
    qr_filename = str(item.pk) + ".png"
    save = False
    if item.qr_code is None: #new item!
        save = True
        url = "/users/" + str(user_id) + "/found/" + str(product_id)
        uri = request.build_absolute_uri(url)
        item.qr_code = uri
        item.save()
    url = item.qr_code
    qr = QRCode(version=20, error_correction=ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make()
    img = qr.make_image()
    if save:
        img.save(settings.MEDIA_ROOT + qr_filename) #TODO: In production, we have to check where the QR image is being saved
    template_url = settings.MEDIA_URL +  qr_filename
    return render(request, 'lostnfound/qr_code.html', {'qr_url': template_url , 'item': item})

#A user wants to change an item's settings
@login_required
def item_settings(request, user_id):
    if request.method == 'POST':
        item_id = request.POST['settings']
        item = Item.objects.get(pk=item_id)
        if 'delete' in request.POST:
            item.delete()
            return HttpResponseRedirect('/users/' + user_id + '/products')
        else:
            redirect = "/users/" + user_id + "/products/" + item_id
            return HttpResponseRedirect(redirect)

    else:
        my_user = User.objects.get(pk=user_id)
        my_items = Item.objects.filter(owner=my_user)
        return render(request, 'lostnfound/settings.html', {'items': my_items })

@login_required
def report_lost(request, user_id):
    if request.method == "POST":
        item_id = request.POST['lost']
        item = Item.objects.get(pk=item_id)
        item.found = False
        item.save()
        return HttpResponseRedirect('/users/' + user_id + '/products')
