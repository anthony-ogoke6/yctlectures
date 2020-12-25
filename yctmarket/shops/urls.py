from django.urls import re_path


from shops import views

app_name = 'shops'

urlpatterns = [
    re_path(r'shop/yctmarket/(?P<id>\d+)/(?P<slug>[\w-]+)$', views.shop_detail, name="shop_detail"),
    re_path(r'product_delete/(?P<id>\d+)/(?P<slug>[\w-]+)/product_delete/$', views.product_delete, name="product_delete"),
    #re_path(r'shop/yctmarket/(?P<id>\d+)/(?P<slug>[\w-]+)$', views.ArticleDetail.as_view(), name="shop_detail"),

]