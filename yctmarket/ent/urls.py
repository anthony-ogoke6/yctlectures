from django.urls import path, re_path


from . import views

app_name = 'ent'

#urlpatterns = [
    #path('', views.article_list, name='home'),
    #url(r'^comment/$', views.comment, name='comment'),
    #path(?P<id>\d+)/post_edit/$', views.post_edit, name="post_edit"),
    #path(?P<id>\d+)/post_delete/$', views.post_delete, name="post_delete"),
    #path(?P<id>\d+)/favourite_post/$', views.favourite_post, name="favourite_post"),
    #path((?P<id>\d+)/(?P<slug>[\w-]+)/$', views.article_details, name="article_details"),
    #path('post_create/$', views.post_create, name="post_create"),
    #path('edit_profile/$', views.edit_profile, name="edit_profile"),
#]
urlpatterns = [
    path('', views.article_list, name='article_list'),
    re_path(r'tag/(?P<tag_slug>[-\w]+)/$', views.article_list, name='post_list_by_tag'),

    re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<amount>\d+)/$', views.advert_details, name="advert_detail"),
    re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/$', views.article_details, name="article_detail"), #using function views here
    #re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<reference>[\w-]+)$', views.shop_detail, name="shop_detail"),
    re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/post_delete/$', views.post_delete, name="post_delete"),
    #re_path(r'product_delete/(?P<id>\d+)/(?P<slug>[\w-]+)/product_delete/$', views.product_delete, name="product_delete"),
    path('edit/', views.edit, name='edit'),



    #re_path('activate/<uidb64>/<token>', yct_views.ActivateAccountView.as_view(), name="activate"),
    #re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/$', views.ArticleDetail.as_view(), name="article_detail"), #using class based views here


]