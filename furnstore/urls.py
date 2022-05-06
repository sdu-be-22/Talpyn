from django.conf import settings
from multiprocessing.dummy import Namespace
from xml.etree.ElementInclude import include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static

urlpatterns = [
        #Leave as empty string for base url
	path('', views.home, name="home"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('register/', views.register, name='register'),
    path('signin/', views.signin, name = 'login'),
	path('signout/', views.signout, name = 'logout'),
    path('profile/', views.profile, name='profile'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
    path('product/',views.product,name='product'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
