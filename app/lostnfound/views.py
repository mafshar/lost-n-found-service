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
from django.core.mail import send_mail
from django.core.signing import Signer
import sys
from qrcode import *

signer = Signer()

#Render the home page
def index(request):
    if request.user.is_authenticated():
        pk = signer.sign(str(request.user.pk))
        return HttpResponseRedirect('./users/' + pk + '/products')
    else:
        return anon_home(request)
def anon_home(request):
    return render(request, 'lostnfound/index.html', {})

#Render the login view
def login_user(request):
    if request.user.is_authenticated():
        pk = signer.sign(str(request.user.pk))
        return HttpResponseRedirect('./users/' + pk + '/products')
    form = AuthenticationForm()
    return render(request, 'lostnfound/login.html', {'form': form})

#Render the signup view
def signup(request):
    if request.user.is_authenticated():
        pk = signer.sign(str(request.user.pk))
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
                new_user.save()
                login(request, new_user)
                pk = signer.sign(str(new_user.pk))
                return HttpResponseRedirect('./users/' + pk + '/products')
            else:
                return render(request, 'lostnfound/signup.html', {'form': form})
        else: #login
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                pk = signer.sign(str(user.pk))
                return HttpResponseRedirect('./users/' + pk + '/products')
            else:
                form = AuthenticationForm()
                return render(request, 'lostnfound/login.html', {'form': form, 'badLogin':True})
    else:
        return HttpResponseRedirect('./')

def logout_view(request):
    logout(request)
    return render(request, 'lostnfound/logged_out.html', {})

#Handles GET & POST by a finder
def handle_lost(request, user_id, product_id):
    if request.method == 'POST':
        finder = FinderForm(request.POST)
        if finder.is_valid():
            finder_name = finder.data['name']
            finder_email = finder.data['email']
            user_id = int(signer.unsign(finder.data['user_id']))
            item_id = int(signer.unsign(finder.data['item_id']))
            item = Item.objects.get(pk=item_id, owner__pk=user_id)
            user = User.objects.get(pk=user_id)
            user_email = user.email
            if item is not None:
                item.found = True
                item.save()
                email_user(user_email, finder_email)
            return render(request, 'lostnfound/thankyou.html',{'item': item})
    else:
        item = Item.objects.get(pk=int(signer.unsign(product_id)))
        user = User.objects.get(pk=int(signer.unsign(user_id)))
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
        my_user = User.objects.get(pk=int(signer.unsign(user_id)))
    except IndexError:
        raise Exception #yikes, there's no user!
    #Find all of user items
    my_items = Item.objects.filter(owner=int(signer.unsign(user_id)))
    show_form = False
    signed_items = {}
    counter = 0
    for item in my_items:
        if item.found is None:
            show_form = True
        new_item = {
        'pk': signer.sign(item.pk),
        'name': item.name,
        'found' : item.found
        }
        signed_items[str(counter)] = new_item
        counter += 1
    context = {
        'user' : my_user,
        'items' : signed_items,
        'show_form' : show_form
    }
    return render(request, 'lostnfound/items.html', context)

#function to generate unique item id that includes user id in the first part
# def generate_item_id(user):
#     user_id = user.pk
#     user_items = Item.objects.filter(owner__pk=user_id)
#     num_of_items = len(user_items) + 1
#     item_id = int(str(user_id) + str(num_of_items))
#
#     return item_id

#Handles a GET and POST for registering an item
@login_required
def register_item(request, user_id):
    my_user = User.objects.get(pk=int(signer.unsign(user_id)))
    if request.method == 'POST':
        form = ItemForm(request.POST)
        new_item = form.save(commit=False)
        new_item.owner = my_user
        new_item.save()
        return HttpResponseRedirect("/users/" + user_id + "/products/" + signer.sign(str(new_item.pk)))
    else:
        form = ItemForm()
        return render(request, 'lostnfound/register_item.html',{'form':form, 'pk': user_id })

@login_required
def print_qr_code(request, user_id, product_id):
    item = Item.objects.get(pk=int(signer.unsign(product_id)))
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
        item = Item.objects.get(pk=int(signer.unsign(item_id)))
        if 'delete' in request.POST:
            item.delete()
            return HttpResponseRedirect('/users/' + user_id + '/products')
        else:
            redirect = "/users/" + user_id + "/products/" + item_id
            return HttpResponseRedirect(redirect)

    else:
        my_user = User.objects.get(pk=int(signer.unsign(user_id)))
        my_items = Item.objects.filter(owner=my_user)
        signed_items = {}
        counter = 0
        for item in my_items:
            new_item = {
            'pk': signer.sign(item.pk),
            'name': item.name
            }
            signed_items[str(counter)] = new_item
            counter += 1
        print signed_items
        print my_items
        return render(request, 'lostnfound/settings.html', {'items': signed_items })

@login_required
def report_lost(request, user_id):
    if request.method == "POST":
        item_id = request.POST['lost']
        item = Item.objects.get(pk=int(signer.unsign(item_id)))
        item.found = False
        item.save()
        return HttpResponseRedirect('/users/' + user_id + '/products')

def email_user(user_email, finder_email):
    '''
    Sends an email to this User.
    '''
    sender = 'noreply.itemfound@gmail.com'
    message = 'Someone has found your lost item! This message will facilitate your item\'s return.'
    if finder_email:
        try:
            send_mail(
                'Your item has been found!',
                message,
                sender,
                [user_email, finder_email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')
