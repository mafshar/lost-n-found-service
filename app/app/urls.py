#Mohammad Afshar, @mafshar, ma2510@nyu.edu
"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from lostnfound import views
from lostnfound.serializers import UserSerializer, ItemSerializer
from django.contrib.auth import views as auth_views



# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^login$', views.login_user, name='login_user'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^users$', views.authenticate_user, name='auth'),
    url(r'^users/(?P<user_id>[0-9]+)/products$', views.user_items, name='user_items'),
    url(r'^users/(?P<user_id>[0-9]+)/new$', views.register_item, name='register_item'),
    url(r'^users/(?P<user_id>[0-9]+)/found/(?P<product_id>[0-9]+)$', views.handle_lost, name='handle_lost'),
    url(r'^users/(?P<user_id>[0-9]+)/products/(?P<product_id>[0-9]+)$', views.delete_item, name='delete_item'),
    url('^', include('django.contrib.auth.urls')),
    # url(r'^users/(?P<user_id>[0-9]+)/products/(?P<product_id>[0-9]+)$', views.report_lost, name='report_lost'),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
