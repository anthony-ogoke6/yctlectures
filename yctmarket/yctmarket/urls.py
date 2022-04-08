from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from ent import views as yct_views
from students import views as students_views
from learn import views as courses_views
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
    path('topic/order/', courses_views.CourseOrderView.as_view(), name='topic_order'),
    ##path('courses/', include('courses.urls', namespace="courses")),
    path('learn/', include('learn.urls', namespace="learn")),
    path('students/', include('students.urls', namespace="students")),
    path('voters/', include('students1.urls', namespace="students1")),
    path('voting/', include('voting.urls', namespace="voting")),
    ##path('api/', include('courses.api.urls', namespace='api')),
    path('', include('ent.urls', namespace="ent")),
    path('', include('shops.urls', namespace="shops")),
    #path('topic/order/', courses_views.CourseOrderView.as_view(), name='topic_order'),
    ##path('courses/', include('courses.urls', namespace="courses")),
    path('students/', include('students.urls', namespace="students")),
    ##path('api/', include('courses.api.urls', namespace='api')),
    #path('', include('users.urls', namespace="users")),
    path('contact/', contact_views.contact_page, name="contact_page"),
    #path('fetch_post/', yct_views.fetch_post, name='fetch_post'),
    path('about/', yct_views.about, name="about"),
    path('thank_you/', yct_views.thank_you, name="thank_you"),
    path('thanks/', yct_views.thanks, name="thanks"),
    path('paystack_confirmation/', yct_views.processPaystackWebhook, name="paystack_confirmation"),
    path('paystack_confirmation2/', students_views.processPaystackWebhook2, name="paystack_confirmation2"),
    path('my_webhook_view/', yct_views.my_webhook_view, name='my_webhook_view'),
    path('login/', yct_views.user_login, name="user_login"),
    #path('post_create/', yct_views.post_create, name="post_create"),
    path('shops/', yct_views.store, name="store"),
    re_path(r'shop/create/(?P<id>\d+)/(?P<slug>[\w-]+)$', yct_views.store_detail, name="store_detail"),

    #path('post_create/', yct_views.post_create, name="post_create"),
    path('plan/', yct_views.plan, name="plan"),
    path('free_month/', yct_views.free_month, name="free_month"),
    path('pay_for_six_month/', yct_views.pay_for_six_month, name="pay_for_six_month"),
    path('pay_for_one_year/', yct_views.pay_for_one_year, name="pay_for_one_year"),
    #path('posts/', yct_views.PostList.as_view(), name="posts"),
    path('cart/', include('cart.urls', namespace='cart')),
    path('pay_per_upload/', yct_views.pay_per_upload, name="pay_per_upload"),
    path('upload_free_at_given/', yct_views.upload_free_at_given, name="upload_free_at_given"),
    re_path(r'upload_product/(?P<store_id>\d+)/(?P<store_slug>[\w-]+)$', yct_views.upload_product, name="upload_product"),
    path('re_request_activation_link/', yct_views.re_request_activation, name="re_request_activation_link"),
    path('activate/<uidb64>/<token>', yct_views.activate, name="activate"),
    path('logout/', yct_views.user_logout, name="user_logout"),
    path('signup/', yct_views.signup_view, name="signup_view"),
    path('signup_students/', yct_views.signup_students_view, name="signup_students"),
    path('signup_choice/', yct_views.signup_choice_view, name="signup_choice"),
    path('signup_tutor/', yct_views.signup_tutor_view, name="signup_tutor_view"),
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

