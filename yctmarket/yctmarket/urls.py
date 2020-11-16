"""enthub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from ent import views as yct_views
from contact import views as contact_views
from django.contrib.sitemaps.views import sitemap
from ent.feeds import LatestPostsFeed

from ent.sitemaps import PostSitemap


sitemaps = {
    'posts': PostSitemap,
    }

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('ent.urls', namespace="ent")),
    #path('', include('users.urls', namespace="users")),
    path('contact/', contact_views.contact_page, name="contact_page"),
    #path('fetch_post/', yct_views.fetch_post, name='fetch_post'),
    path('about/', yct_views.about, name="about"),
    path('thank_you/', yct_views.thank_you, name="thank_you"),
    path('thanks/', yct_views.thanks, name="thanks"),
    path('paystack_confirmation/', yct_views.processPaystackWebhook, name="paystack_confirmation"),
    path('my_webhook_view/', yct_views.my_webhook_view, name='my_webhook_view'),
    path('login/', yct_views.user_login, name="user_login"),
    #path('post_create/', yct_views.post_create, name="post_create"),
    path('plan/', yct_views.plan, name="plan"),
    #path('posts/', yct_views.PostList.as_view(), name="posts"),
    #path('cart/', include('cart.urls', namespace='cart')),
    path('pay_per_upload/', yct_views.pay_per_upload, name="pay_per_upload"),
    path('upload_free_at_given/', yct_views.upload_free_at_given, name="upload_free_at_given"),
    path('re_request_activation_link/', yct_views.re_request_activation, name="re_request_activation_link"),
    path('activate/<uidb64>/<token>', yct_views.activate, name="activate"),
    path('logout/', yct_views.user_logout, name="user_logout"),
    path('signup/', yct_views.signup_view, name="signup_view"),
    #path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('sitemap\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('feed/',  LatestPostsFeed(), name='post_feed'),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

