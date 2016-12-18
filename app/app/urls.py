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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static



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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^login$', views.login_user, name='login_user'), #render login template
    # url(r'^logout$', views.logout_view, name='logout'), #render logout template
    url(r'^signup$', views.signup, name='signup'), #render signup template
    url(r'^users$', views.authenticate_user, name='authenticate_user'), #POST for login/signup
    url(r'^users/(?P<user_id>.*)/report/products$', views.report_lost, name='report_lost'), #POST for user reporting a lost item
    url(r'^users/(?P<user_id>.*)/products$', views.user_items, name='user_items'), #render user items
    url(r'^users/(?P<user_id>.*)/new$', views.register_item, name='register_item'), #GET & POST for registering a new item
    url(r'^users/(?P<user_id>.*)/products/settings', views.item_settings, name='item_settings'), #GET & POST for item settings
    url(r'^users/(?P<user_id>.*)/products/(?P<product_id>.*)$', views.print_qr_code, name='print_qr_code'), #renders view for QR code
    url(r'^users/(?P<user_id>.*)/found/(?P<product_id>.*)$', views.handle_lost, name='handle_lost'), #GET & POST for a finder scanning a QR code
    url('^', include('django.contrib.auth.urls')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_URL)
