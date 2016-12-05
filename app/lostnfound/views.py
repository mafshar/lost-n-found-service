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
import sys
#import pyqrcode
import qrcode

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
def signup(request):
    signup = MyUserCreationForm()
    return render(request, 'lostnfound/signup.html', {'form': signup})

#Handles a signup
def authenticate_user(request):
    if request.method == 'POST':
        #get user data from post request
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=True)
            login(request, new_user)
            pk = str(new_user.pk)
            return HttpResponseRedirect('./users/' + pk + '/products')
        else:
            return HttpResponseRedirect('./signup')
    else:
        return HttpResponseRedirect('./signup')

#Handles GET & POST by a finder
def handle_lost(request, user_id, product_id):
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
        item = Item.objects.get(pk=user_id)
        data = {
            'user_id': user_id,
            'item_id': product_id,
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

#function to generate unique item id that includes user id in the first part
@login_required
def generate_item_id(user):
 
    user_id = user.id
    user_items = Item.objects.filter(owner=user)
    num_of_items = len(user_items) + 1
    item_id = int(str(user_id) + str(num_of_item))

    return item_id

#Handles a GET and POST for registering an item
@login_required
def register_item(request, user_id):

    try:
	my_user = User.objects.get(user=request.user)
    except IndexError:
	raise Exception #yikes, there's no user!

    if request.method == 'POST':
        form = ItemForm(request.POST)
        new_item = form.save(commit=False) #Need to save the db object now in order to access its id.
        new_item.owner = my_user
	new_item.found = NULL
	new_item.item_id = generate_item_id(my_user)
	new_item.save()

        #Constructing URL for QR code
        #url = 'http://myapp.com/users/' + str(request.user.pk) + '/found/' + str(new_item.pk) #FIXME: what's the hostname for our web app?
        # new_item.qr_code = generate_qr(new_item.id) #TODO: I need the function call to generate the QR code!
	
	#TODO: edit later to include hostname for app
	url = '/recovered/' + str(new_item.item_id) + '/'
	uri = request.build_absolute_uri(url)

        #return print_qr_code(request, url, new_item.pk)
	return print_qr_code(request, uri, new_item.item_id)

    else:
        form = ItemForm()
        return render(request, 'lostnfound/register_item.html',{'form':form, 'user': my_user })

@login_required
def print_qr_code(request, url, new_item):

    #qr = pyqrcode.create(url)
    #qr_filename = str(new_item) + '.png'
    #qr.png(qr_filename, scale=5)

    qr = qrcode.make(url)
    qr_filename = str(new_item) + '.png'
    qr.save(settings.MEDIA_ROOT + qr_filename)

    return render(request, 'lostnfound/qr_code.html', {'qr_url': settings.MEDIA_URL + qr_filename, 'item': new_item}) 


#TODO: IMPLEMENT ME!
#A user wants to delete an item.
@login_required
def delete_item(request, user_id, product_id):
    #delete the item based on the user and the primary key
    delete_item = Item.objects.get(pk=request.item) #TODO: Figure out how to handle filtering using a foreign key's primary key
    delete_item.delete()
    return user_items(request)

#TODO: IMPLEMENT ME!
@login_required
def report_lost(request, user_id, product_id):
    return HttpResponse("Hello! I'm still in the process of being implemented.")
