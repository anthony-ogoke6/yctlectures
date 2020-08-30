
from .forms import *
from .forms import EmailFormForMeetUp, EmailFormForPayment, InfiniteScrollForm, PostCreateForm, PostCreateFormForFree, UserLoginForm, UserRegistrationForm, ReRequestActivationForm
import requests
import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
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
from .utils import generate_token

from .models import Article, Profile, Reference, Post, AdvertImages, PurchaseReference, PhoneNumber, Images
import datetime
import hmac
import hashlib
import json



def paystack_confirmation(request):
    # paystack_sk = "sk_liveffb5db8bf8d3abe7f343a743ae58ac5911c68d11"
    '''
    The function takes an http request object containing the json data
    from paystack webhook client. Django's http request and response
    object was used for this example
    '''
    paystack_sk = "sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111"
    json_body = json.loads(request.body)
    computed_hmac = hmac.new(
        bytes(paystack_sk, 'utf-8'),
        str.encode(request.body.decode('utf-8')),
        digestmod=hashlib.sha512
        ).hexdigest()
    if 'HTTP_X_PAYSTACK_SIGNATURE' in request.META:
        if request.META['HTTP_X_PAYSTACK_SIGNATURE'] == computed_hmac:
            #res = request.json()
            status = json_body['data']['status']
            if status == "success":
                reference = json_body['data']['reference']
                user_reference = Reference(user_reference_number=reference)
                user_reference.save()
                articles = Article.published.all()
                for article in articles:
                    if article.reference == reference:
                        title = article.title
                        slug  = article.slug
                        status = article.status
                        author = article.author
                        amount = article.amount
                        category = article.category
                        description = article.description
                        video = article.video
                        image = article.image
                        bodysnippet = article.bodysnippet
                        body = article.body
                        image2 = article.image2
                        image3 = article.image3
                        view_count = article.view_count
                        duration = article.duration
                        created = article.created
                        updated = article.updated

                        post = Post(
                            reference=reference, title=title, slug=slug, status=status, author=author,
                            amount=amount, category=category, description=description, video=video,
                            image=image, bodysnippet=bodysnippet, body=body, image2=image2, image3=image3,
                            view_count=view_count, duration=duration, created=created, updated=updated
                        )
                        post.save()
                        return HttpResponse(status=200)

    return HttpResponse(status=400)

def article_list(request):
    pics = AdvertImages.objects.all()
    pic = Images.objects.all()
    context = {
        'pics':pics,
        'pic':pic,
        }
    return render(request, 'ent/article_list.html', context )

def fetch_post(request):
    limit = request.GET.get('limit')
    start = request.GET.get('start')

    #empty dict
    #data = []

    #data = []

    #querry all post in Post model
    search = request.GET.get('q')
    article = Post.published.all()[int(start):int(limit)]
    query = request.GET.get('q')
    if query:
        article = Post.published.filter(
        Q(title__icontains=query)|
        Q(category__icontains=query)
        )





    context = {
        'article': article,
        'search': search,
    }



    return render(request, 'ent/fetch_article_list.html', context)





def article_details(request, id, slug):
    post_increament = get_object_or_404(Post, id=id, slug=slug)
    post_increament.view_count +=1
    post_increament.save()
    related = []
    post = get_object_or_404(Post, id=id, slug=slug)
    url = f"https://yctmarket.pythonanywhere.com{post.image.url}"
    q = post.title
    author = post.author
    amount = post.amount
    title = post.title
    # if int(post.amountInDols) > 1:

    #     urls = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    #     req = requests.request("GET", urls)
    #     print(req)
    #     amount = None

    # else:
    #     amount = post.amount



    similar = Post.published.filter(
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
        print("it got here")
        form = EmailFormForPayment(request.POST or None)
        print(form)

        #if form.is_valid():
        lastnme = request.POST.get('lastname')
        print("check if this lastnme will show")
        print(lastnme)
        firstname = request.POST['firstname']
        print(firstname)
        lastname = form.cleaned_data['lastname']

        print(lastname)
        email = form.cleaned_data['email']
        print(email)
        address = form.cleaned_data['address']
        print(address)
        phoneNumber = form.cleaned_data['phoneNumber']
        print("it got here too")
        print(phoneNumber)
        subject = f"Customer about to pay for {post.title} at yctmarket"
        message = '%s %s %s %s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber, author, amount, title)
        emailFrom = [settings.EMAIL_HOST_USER]
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
        #checkout = res['data']['authorization_url']
        #return redirect(checkout)
        return redirect('thanks')

            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = EmailFormForPayment()

    context = {
        'post': post,
        'amount': amount,
        'url' : url,
        'form' : form,
        'related':related,
    }

    return render(request, 'ent/article_detail.html', context)


def advert_details(request, id, slug, amount):
    post_increament = get_object_or_404(AdvertImages, id=id, slug=slug, amount=amount)
    post_increament.view_count +=1
    post_increament.save()
    related = []
    post = get_object_or_404(AdvertImages, id=id, slug=slug, amount=amount)
    url = f"https://yctmarket.pythonanywhere.com{post.pic.url}"
    q = post.title



    similar = Post.published.filter(
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


    context = {
        'post': post,
        'url' : url,
        'related':related,
    }

    return render(request, 'ent/advert_detail.html', context)




class ArticleDetail(View):

    def get(self, request, id, slug):
        related = []
        post_increament = get_object_or_404(Post, id=id, slug=slug)

        post_increament.view_count +=1
        post_increament.save()
        post = get_object_or_404(Post, id=id, slug=slug)
        url = f"https://yctmarket.pythonanywhere.com/{post.image.url}"
        q = post.title


        similar = Post.published.filter(
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



        #if post.duration:
            #form = None
            #form = EmailFormForMeetUp()
        #else:
        form = EmailFormForPayment()

        context = {
            'post': post,
            'url' : url,
            'form' : form,
            'related':related,

        }
        return render(request, 'ent/article_detail.html', context)


    def post(self, request, id, slug):
        post = get_object_or_404(Post, id=id, slug=slug)
        postTitle = post.title
        #if 'email' in request.POST:
        form = EmailFormForPayment(request.POST or None)
        print('firstname')
        if form.is_valid():
            print("what is really going on")
            firstname = form.cleaned_data['firstname']
            print(firstname)
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phoneNumber = form.cleaned_data['phoneNumber']
            subject = f"Customer about to pay for your {postTitle} product at yctmarket.com"
            message = '%s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber)
            emailFrom = [settings.EMAIL_HOST_USER]
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            return redirect('thanks')


        return redirect('thanks')



def article_detail(request, id, slug):
    post_increament = get_object_or_404(Post, id=id, slug=slug)
    post_increament.view_count +=1
    post_increament.save()
    related = []
    post = get_object_or_404(Post, id=id, slug=slug)
    url = f"https://yctmarket.pythonanywhere.com{post.image.url}"
    q = post.title


    similar = Post.published.filter(
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
    postTitle = post.title
    if request.method == 'POST':
        print("it got here")
        form = EmailFormForPayment(request.POST or None)

        if form.is_valid():
            firstname = request.POST['firstname']
            print(firstname)
            lastname = form.cleaned_data['lastname']
            print(lastname)
            email = form.cleaned_data['email']
            print(email)
            address = form.cleaned_data['address']
            print(address)
            phoneNumber = form.cleaned_data['phoneNumber']
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
                     'Authorization': 'Bearer sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111',
                     'Content-Type': 'application/json',
                }


            data = {"reference": reference, "amount": amount, "email": email}
            url = "https://api.paystack.co/transaction/initialize"
            response = requests.request("POST", url, headers=headers, json=data)
            res = response.json()

            checkout = res['data']['authorization_url']
            #return redirect(checkout)
            return redirect('thanks')

    else:
        form = EmailFormForPayment()
    context = {
        'post': post,
        'url' : url,
        'form' : form,
        'related':related,
    }
    #return render(request, 'ent/upload_free_at_given.html', context)
    return render(request, 'ent/article_detail.html', context)





def detail(request, id, slug):
    post_increament = get_object_or_404(Post, id=id, slug=slug)
    post_increament.view_count +=1
    post_increament.save()
    related = []
    post = get_object_or_404(Post, id=id, slug=slug)
    url = f"https://yctmarket.pythonanywhere.com{post.image.url}"
    q = post.title


    similar = Post.published.filter(
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
    postTitle = post.title
    if request.method == 'POST':
        form = form = EmailFormForPayment(request.POST or None)

        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phoneNumber = form.cleaned_data['phoneNumber']
            subject = 'Customer about to pay at yctmarket'
            message = '%s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber)
            emailFrom = [settings.EMAIL_HOST_USER]
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

            r = PurchaseReference(firstname=firstname, lastname=lastname, email=email)
            reference = str(r.reference)
            r.save()

            headers = {
                     'Authorization': 'Bearer sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111',
                     'Content-Type': 'application/json',
                }


            data = {"reference": reference, "amount": amount, "email": email}
            url = "https://api.paystack.co/transaction/initialize"
            response = requests.request("POST", url, headers=headers, json=data)
            res = response.json()

            checkout = res['data']['authorization_url']
            #return redirect(checkout)
            return redirect('thanks')

    else:
        form = EmailFormForPayment()





    context = {
        'post': post,
        'url' : url,
        'form' : form,
        'related':related,

    }
    return render(request, 'ent/article_detail.html', context)



def about(request):
    context = {}
    template = 'ent/about.html'
    return render(request,template,context)


def thank_you(request):
    context = {}
    template = 'ent/thank_you.html'
    return render(request,template,context)


def thanks(request):
    context = {}
    template = 'ent/thanks.html'
    return render(request,template,context)


def plan(request):
    context = {}
    template = 'ent/plan.html'
    return render(request,template,context)

def re_request_activation(request):
    user_email = []
    if request.method == 'POST':
        form = ReRequestActivationForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.all()
            for user in users:
                user_email.append(user.email)
                if email in user_email:
                    saved_user = User.objects.get(email=email)
                    current_site = get_current_site(request)
                    email_subject = 'Activate your account'
                    message = render_to_string("ent/activate.html",
                        {
                            'user':saved_user,
                            'domain':current_site.domain,
                            #'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                            'uid': urlsafe_base64_encode(force_bytes(saved_user.pk)).decode(),
                            'token': generate_token.make_token(saved_user)
                        }

                        )

                    email_message = EmailMessage(
                        email_subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email]
                    )

                    email_message.send()

                    messages.add_message(request, messages.SUCCESS, 'An activation email has been sent to you.')
                    return redirect('user_login')
                else:
                    messages.add_message(request, messages.INFO, 'Email not registered. You can click on <bold>sign up</bold> to register.')
                    return redirect('user_login')
    else:
        form = ReRequestActivationForm()
    context = {
        'form': form,
    }
    return render(request, "ent/rerequest_activation.html", context)



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            email = form.cleaned_data['email']
            #firstname = form.cleaned_data['firstname']
            #lastname = form.cleaned_data['lastname']
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phoneNumber']
            password = form.cleaned_data['password1']
            new_user.set_password(form.cleaned_data['password1'])
            #new_user.is_active=False
            new_user.save()
            saved_user = User.objects.get(username=username)
            user_phone = PhoneNumber(user=saved_user, phone_number=phone_number)
            user_phone.save()
            Profile.objects.create(user=new_user)
            subject = f"Seller name {username} just registered at yctmarket"
            message = '%s %s ' %(email, phone_number)
            emailFrom = [settings.EMAIL_HOST_USER]
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.POST:
                        messages.add_message(request, messages.SUCCESS, 'Account created successfully.')
                        return HttpResponseRedirect(reverse(request.POST.get('next')))
                    else:
                        messages.add_message(request, messages.SUCCESS, 'Account created successfully.')
                        return HttpResponseRedirect(reverse('ent:article_list'))
                else:
                    return HttpResponse("User is not active")
            else:
                return HttpResponse("User is None")

            #messages.add_message(request, messages.SUCCESS, 'Account created successfully. An activation email has been sent to you.')
            #return redirect('user_login')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, "ent/register.html", context)


# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except Exception as identifier:
#             user = None


#         if user is not None and generate_token.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.add_message(request, messages.INFO, 'account activated successfully')
#             return redirect('user_login')
#         return render(request, "ent/activate_failed.html", status=401)



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        #uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model(pk=uid)
        print('checking if the error is from the uid')
        print(uid)
        print("generating token")
        print(generate_token.check_token(user, token))
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print("failure to work")
    if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, 'Account activated successfully. Now you can login your account.')
            return redirect('user_login')
    else:
        return render(request, "ent/activate_failed.html", status=401)



@login_required(login_url="user_login")
def upload_free_at_given(request):
    user = request.user
    if request.method == 'POST':
        form = PostCreateFormForFree(request.POST, request.FILES)
        if form.is_valid():
            r = uuid.uuid4()
            reference = str(r)
            post = form.save(commit=False)
            post.author = request.user
            title = post.title
            amount = post.amount
            post.reference = reference
            post.save()
            subject = f"{user} just made a new post on yctmarket"
            message = '%s %s %s ' %(title, amount, user)
            emailFrom = [settings.EMAIL_HOST_USER]
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            messages.success(request, "Post has been successfully created.")
            return redirect('ent:article_list')
    else:
        form = PostCreateFormForFree()
    context = {
        'form': form,
    }
    return render(request, 'ent/upload_free_at_given.html', context)







@login_required(login_url="ogokeanthony187scrumy:login")
def pay_per_upload(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():

            title = request.POST['title']
            duration = int(request.POST['duration'])
            category = request.POST['category']
            amount = request.POST['amount']
            description = request.POST['description']
            r = uuid.uuid4()
            reference = str(r)


            post = form.save(commit=False)
            post.author = request.user
            post.reference = reference
            post.save()
            #article = Article.objects.filter(reference=reference)
            #reference = str(article[0].reference)
            email = request.user.email
            name = request.user.username
            number = request.user.phoneNumber
            print(name)
            print(number)

            headers = {
                'Authorization': 'Bearer FLWSECK-775e1a45406c76dc400f8cb52db4c62f-X',
                'Content-Type': 'application/json',
            }

            if duration == 7:
                price = 40000
            elif duration == 14:
                price = 80000
            elif duration == 21:
                price = 120000
            elif duration == 28:
                price = 160000
            elif duration == 31:
                price = 200000
            else:
                price = 14640000

            payment = price

            #data = {"tx_ref": reference, "amount":payment, "email":email}
            data = {
               "tx_ref":reference,
               "amount":payment,
               "currency":"NGN",
               "redirect_url":"https://yctmarket.pythonanywhere.com/thank_you/",
               "payment_options":"card",
               "customer":{
                  "email":email,
                  "phonenumber":number,
                  "name":name
               },
               "customizations":{
                  "title":"Pay per upload",
                  "description":"Customers pay a token to upload their product",
                  "logo":"https://yctmarket.pythonanywhere.com/static/img/yctmarket.png"
               }
            }
            url = "https://api.flutterwave.com/v3/payments"
            response = requests.request("POST", url, headers=headers, json=data)

            #response = requests.post('https://api.paystack.co.transaction/initialize', headers=headers, json=data)
            res = response.json()

            checkout = res['data']['link']

            return redirect(checkout)

    else:
        form = PostCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'ent/pay_per_upload.html', context)








def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('ent:article_list'))
                else:
                    messages.info(request, 'User not active, re-request your activation link')
                    return HttpResponseRedirect(reverse('ent:re_request_activation_link'))
            else:
                messages.error(request, 'Information provided not correct. Check username or password or check your email to activate your account.')
                form = UserLoginForm()
                context = {
                    'form': form,
                }
                return render(request, 'ent/login.html', context)
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'ent/login.html', context)








def user_logout(request):
    logout(request)
    return redirect('ent:article_list')