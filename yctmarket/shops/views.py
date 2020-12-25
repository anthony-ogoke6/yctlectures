
from ent.forms import *
from ent.forms import EmailFormForMeetUp, EmailFormForPayment, InfiniteScrollForm, PostCreateForm, PostCreateFormForFree, UserLoginForm, UserRegistrationForm, ReRequestActivationForm, CommentForm, ProfileForm, UserEditForm, ProfileEditForm,  ShopFreeForOneMonth, ShopPaymentSixMonth, UploadProductForFree, ShopPaymentOneYearMonth
import requests
import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, CreateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views import View
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from validate_email import validate_email
from django.core.mail import send_mail, EmailMessage
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from ent.utils import generate_token
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from ent.models import Article, Profile, Reference, Post, AdvertImages, PurchaseReference, PhoneNumber, Images, Comment
from shops.models import Stores, Shops, NamesOfPeopleWhoHaveOwnedShops, Product
import datetime
from taggit.models import Tag
from django.db.models import Count
import hmac
import hashlib
import json

import logging
# Create your views here.





def shop_detail(request, id, slug):
    post_increament = get_object_or_404(Product, id=id, slug=slug)
    post_increament.view_count +=1
    post_increament.save()
    related = []
    post = get_object_or_404(Product, id=id, slug=slug)
    url = f"https://yctmarket.pythonanywhere.com{post.image.url}"
    q = post.title
    search = request.GET.get('search')
    if search:
        post = Product.published.filter(
            Q(title__icontains=search)|
            Q(author__icontains=search)|
            Q(store__icontains=search)|
            Q(description__icontains=search)
            )
    similar = Product.published.filter(
    Q(title__icontains=q)|
    Q(category__icontains=q)
    )
    if len(similar)==2:
        related.append(similar[1])

    elif len(similar)==3:
        related.append(similar[1])
        related.append(similar[2])
    elif len(similar)>3:
        related.append(similar[1])
        related.append(similar[2])
        related.append(similar[3])



    amount = post.amount
    print(amount)
    postTitle = post.title
    if request.method == 'POST':
        print("it got here")
        form = EmailFormForPayment(request.POST or None)

        #if form.is_valid():
        firstname = request.POST['firstname']
        print(firstname)
        lastname = request.POST['lastname']
        print(lastname)
        email = request.POST['email']
        print(email)
        quantity = request.POST['quantity']
        print(quantity)
        amount = int(str(post.amount) + "00") * int(quantity)
        address = request.POST['address']
        print(address)
        phoneNumber = request.POST['phoneNumber']
        print("it got here too")
        print(phoneNumber)
        subject = 'Customer about to pay at yctmarket'
        message = '%s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber)
        emailFrom = [settings.EMAIL_HOST_USER]
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

        r = PurchaseReference(firstname=firstname, lastname=lastname, email=email)
        reference = str(r.reference)
        r.save()

        headers = {
                'Authorization': 'Bearer sk_live_ffb5db8bf8d3abe7f343a743ae58ac5911c68d11',
                'Content-Type': 'application/json',
            }


        data = {"reference": reference, "amount": amount, "email": email}
        url = "https://api.paystack.co/transaction/initialize"
        response = requests.request("POST", url, headers=headers, json=data)
        res = response.json()

        checkout = res['data']['authorization_url']
        return redirect(checkout)
        #return redirect('thanks')

    else:
        form = EmailFormForPayment()
    context = {
        'post': post,
        'amount': amount,
        'url' : url,
        'form' : form,
        'related':related,
        #'similar_posts': similar_posts
    }

    return render(request, 'ent/shop_detail.html', context)



def product_delete(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    if request.user != product.author:
        raise Http404()
    product.delete()
    store = Stores.objects.get(owner=request.user or None)
    messages.error(request, "Product has been successfully deleted")
    return redirect("store_detail", id=store.id, slug=store.slug)




