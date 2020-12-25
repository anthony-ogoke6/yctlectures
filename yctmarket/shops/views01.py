
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



def shop_detail(request, id, slug, reference):
    post_increament = get_object_or_404(Product, id=id, slug=slug, reference=reference)
    post_increament.view_count +=1
    post_increament.save()
    related = []
    post = get_object_or_404(Product, id=id, slug=slug, reference=reference)
    print(post)
    url = f"https://yctmarket.pythonanywhere.com{post.image.url}"
    q = post.title
    amount = post.amount

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
     .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
     .order_by('-same_tags','-created')[:3]



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




    if request.method == 'POST':
        form = EmailFormForPayment(request.POST or None)
        print('checking if there is a post request')
        if form.is_valid():
            print('checking if form is valid')
            fr = form.save(commit=False)
            lastnme = request.POST.get('lastname')
            firstname = request.POST['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phoneNumber = form.cleaned_data['phoneNumber']

            payment = post.amount




            r = PurchaseReference(firstname=firstname, lastname=lastname, email=email)
            reference = str(r.reference)
            r.save()


            fr.reference = reference
            fr.save()
            author = post.author
            title = post.title
            amount = int(str(post.amount) + "00")



            subject = f"Customer about to pay for {post.title} at yctmarket"
            message = '%s %s %s %s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber, author, amount, title)
            emailFrom = [settings.EMAIL_HOST_USER]
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            print('checking if it will reach here')



            headers = {
                        'Authorization': 'Bearer sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111',
                        'Content-Type': 'application/json',
                    }

            data = {"reference": reference, "amount":payment, "email":email}
            url = "https://api.paystack.co/transaction/initialize"
            response = requests.request("POST", url, headers=headers, json=data)

            #response = requests.post('https://api.paystack.co.transaction/initialize', headers=headers, json=data)
            res = response.json()
            print('checking for the value of res')
            print(res)

            checkout = res['data']['authorization_url']

            return redirect(checkout)

    else:
        form = EmailFormForPayment()
    context = {
        'post': post,
        'amount': amount,
        'url' : url,
        'form' : form,
        'related':related,
        'similar_posts': similar_posts
    }

    return render(request, 'ent/shop_detail.html', context)


