from django.urls import path, re_path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('cart_add/', views.cart_add, name='cart_add'),
    #re_path(r'add/(?P<post_id>\d+)/(?P<post_slug>[\w-]+)/$', views.cart_add, name='cart_add'),
    re_path(r'remove/(?P<post_id>\d+)/$', views.cart_remove, name='cart_remove'),
]
