
from .forms import EmailFormForMeetUp, EmailFormForPayment, InfiniteScrollForm, PostCreateForm, PostCreateFormForFree, UserLoginForm, UserRegistrationForm
import requests
import uuid
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.forms.models import model_to_dict
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

from .models import Article, Profile, Reference, Post, AdvertImages, PurchaseReference, Stores, Category
from cart.cart import Cart
from cart.forms import CartAddProductForm
import datetime, time
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
    paystack_sk = "sk_live_ffb5db8bf8d3abe7f343a743ae58ac5911c68d11"
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
                print("this is the list of articles")
                print(articles)
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
                        subject = f"pay per upload payment. Post Title: {post.title} product at yctmarket.com"
                        message = 'checking to see if paystack sent a webhook message.'
                        emailFrom = [settings.EMAIL_HOST_USER]
                        emailTo = [settings.EMAIL_HOST_USER]
                        send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

                        return HttpResponse(status=200)

    return HttpResponse(status=400)



class PostList(View):
    def get(self, request):
        print("request.GET starts here")
        print(request)
        #empty list
        articles = []

        posts = Post.published.all()

        #iterate for post in posts and check if duration exceeded or not
        for post in posts:
            #check post duration for each post
            if post.duration:

                #check when post was created
                post_created = post.created.date()

                #check todays date
                todays_date = datetime.date.today()

                #subtract the date when post was created from todays date to get amount of days left for post to remain on blog
                days_left = todays_date - post_created

                #check if the days left is greater or equal to the post's duration
                if days_left.days >= post.duration:

                    #if duration exceeded delete post
                    post.delete()
                else:
                    #if duration not exceeded, append post to articles list
                    articles.append(post)
            else:
                #if post doesnt have duration, append to article list
                articles.append(post)


        pics =  AdvertImages.objects.all()
        pic = pics[0]
        pic1 = pics[1]
        #data = articles[:6]


        context = {
        #'content': content,
        'pic': pic,
        'pic1': pic1,
        #'data': data,
        }



        return render(request, 'ent/article_list.html', context)

    def post(self, request):
        #empty list
        articles = []

        #empty dict
        #data = {}

        data = []

        #querry all post in Post model
        posts = Post.published.all()

        #iterate for post in posts and check if duration exceeded or not
        for post in posts:
            #check post duration for each post
            if post.duration:

                #check when post was created
                post_created = post.created.date()

                #check todays date
                todays_date = datetime.date.today()

                #subtract the date when post was created from todays date to get amount of days left for post to remain on blog
                days_left = todays_date - post_created

                #check if the days left is greater or equal to the post's duration
                if days_left.days >= post.duration:

                    #if duration exceeded delete post
                    post.delete()
                else:
                    #if duration not exceeded, append post to articles list
                    articles.append(post)
            else:
                #if post doesnt have duration, append to article list
                articles.append(post)

        #get an instance of infinte scrol form and save request.POST in variable named form
        form = InfiniteScrollForm(request.POST)


        #check if form is valid
        if form.is_valid():
            #get the value of start
            start = form.cleaned_data['start']
            print('start begings here' + str(start))

            #get the value of end
            end = form.cleaned_data['end']
            print('end begings here' + str(end))


            #iterate through the range of start and end and for each number take article[i] and append in another list called data

            for i in range(start, end + 1):
                if i < len(articles):
                    data.append(articles[i])


            page = request.GET.get('page', 1)
            paginator = Paginator(data, 6)

            try:
                articles = paginator.page(page)
            except PageNotAnInteger:
                articles = paginator.page(1)
            except EmptyPage:
                articles = paginator.page(paginator.articles_list)

            context = {
                'articles': articles,
                }




        time.sleep(1)

        #return JsonResponse(serializers.serialize("json", data), safe=False)
        return context





def stores(request):
    stores = Stores.objects.all()
    query = request.GET.get('q')
    if query:
        stores = Stores.published.filter(
        Q(title__icontains=query)|
        Q(category__icontains=query)
        )




    paginator = Paginator(stores, 6)
    page = request.GET.get('page')
    try:
        stores = paginator.page(page)
    except PageNotAnInteger:
        stores = paginator.page(1)
    except EmptyPage:
        stores = paginator.page(paginator.num_pages)



    context = {
        'stores': stores,
    }

    return render(request, 'ent/shops.html', context)






def article_list(request):
    pics =  AdvertImages.objects.all()
    pic = pics[0]
    pic1 = pics[1]


    articles = []

    #empty dict
    #data = []

    #data = []

    #querry all post in Post model
    search = request.GET.get('q')
    posts = Post.published.all()
    query = request.GET.get('q')
    if query:
        posts = Post.published.filter(
        Q(title__icontains=query)|
        Q(category__icontains=query)
        )

    #iterate for post in posts and check if duration exceeded or not
    for post in posts:
        #check post duration for each post
        if post.duration:

            #check when post was created
            post_created = post.created.date()

            #check todays date
            todays_date = datetime.date.today()

            #subtract the date when post was created from todays date to get amount of days left for post to remain on blog
            days_left = todays_date - post_created

            #check if the days left is greater or equal to the post's duration
            if days_left.days >= post.duration:

                #if duration exceeded delete post
                post.delete()
            else:
                #if duration not exceeded, append post to articles list
                articles.append(post)
        else:
            #if post doesnt have duration, append to article list
            articles.append(post)


    paginator = Paginator(articles, 6)
    page = request.GET.get('page')
    try:
        article = paginator.page(page)
    except PageNotAnInteger:
        article = paginator.page(1)
    except EmptyPage:
        article = paginator.page(paginator.num_pages)



    context = {
        'article': article,
        #'content': content,
        'pic': pic,
        'pic1': pic1,
        'search': search,
    }



    return render(request, 'ent/article_list.html', context)








class ArticleDetail(View):

    def get(self, request, id, slug):
        related = []
        post_increament = get_object_or_404(Post, id=id, slug=slug)

        post_increament.view_count +=1
        post_increament.save()
        post = get_object_or_404(Post, id=id, slug=slug)
        print("ths is the post id")
        print(post.id)
        url = f"https://yctmarket.pythonanywhere.com/{post.image.url}"
        q = post.title


        similar = Post.published.filter(
        Q(title__icontains=q)|
        Q(category__icontains=q)
        )

        if len(similar)>2:
            related.append(similar[2])
            if len(similar)>3:
                related.append(similar[3])
                if len(similar)>4:
                    related.append(similar[4])




        form = EmailFormForPayment()

        context = {
            'post': post,
            'url' : url,
            'form' : form,
            'related':related,

        }
        return render(request, 'ent/article_detail.html', context)


    def post(self, request, id, slug):
        post_increament = get_object_or_404(Post, id=id, slug=slug)

        post_increament.view_count +=1
        post_increament.save()
        post = get_object_or_404(Post, id=id, slug=slug)
        url = f"https://yctmarket.pythonanywhere.com{post.image.url}"



        amount = post.amount
        postTitle = post.title
        if 'email' in request.POST:
            form = EmailFormForPayment(request.POST or None)

            if form.is_valid():
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                phoneNumber = form.cleaned_data['phoneNumber']
                subject = f"Customer about to pay for your {postTitle} product at yctmarket.com"
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
                return redirect(checkout)

        return redirect('thank_you')





class CheckoutDetail(View):

    def get(self, request, id, slug):
        post_increament = get_object_or_404(Post, id=id, slug=slug)

        post_increament.view_count +=1
        post_increament.save()
        post = get_object_or_404(Post, id=id, slug=slug)
        url = f"https://yctmarket.pythonanywhere.com/{post.image.url}"

        if post.duration:
            form = EmailFormForMeetUp()
        else:
            form = EmailFormForPayment()

        context = {
            'post': post,
            'url' : url,
            'form' : form,

        }
        return render(request, 'ent/article_detail.html', context)


    def post(self, request, id, slug):
        post_increament = get_object_or_404(Post, id=id, slug=slug)

        post_increament.view_count +=1
        post_increament.save()
        post = get_object_or_404(Post, id=id, slug=slug)
        url = f"https://yctmarket.pythonanywhere.com{post.image.url}"



        amount = int(str(post.amount) + "00")

        postTitle = post.title
        if 'email' in request.POST:
            form = EmailFormForPayment(request.POST or None)

            if form.is_valid():
                firstname = form.cleaned_data['firstname']
                print(firstname)
                lastname = form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                phoneNumber = form.cleaned_data['phoneNumber']
                print(phoneNumber)
                subject = f"Customer about to pay for your {post.title} product at yctmarket.com"
                message = '%s %s %s %s %s %s ' %(postTitle, firstname, lastname, email, address, phoneNumber)
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
                return redirect(checkout)
        else:
            form = EmailFormForMeetUp(request.POST or None)

            if form.is_valid():
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                phoneNumber = form.cleaned_data['phoneNumber']
                subject = f"A potential customer from yctmarket.com has interest in your {post.title} product"
                message = '%s %s %s %s %s %s ' %(postTitle, firstname, lastname, email, address, phoneNumber)
                emailFrom = [settings.EMAIL_HOST_USER]
                emailTo = post.author.email
                send_mail(subject, message, emailFrom, emailTo, fail_silently=True )


                subject1 = f"A potential customer from yctmarket.com has interest in the {post.title} product /n Custumer FirstName: {firstname} /n Customer LastName: {lastname} /n Customer Address: {address} /n Customer Number: {phoneNumber}"
                message2 = '%s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber)
                emailFrom2 = [settings.EMAIL_HOST_USER]
                emailTo2 = [settings.EMAIL_HOST_USER]
                send_mail(subject1, message2, emailFrom2, emailTo2, fail_silently=True )


        return redirect('thanks')


class StoreDetail(View):

    def get(self, request, id, slug):
        post_increament = get_object_or_404(Stores, id=id, slug=slug)

        post_increament.view_count +=1
        post_increament.save()
        post = get_object_or_404(Post, id=id, slug=slug)
        url = f"https://yctmarket.pythonanywhere.com/{post.image.url}"

        if post.duration:
            form = EmailFormForMeetUp()
        else:
            form = EmailFormForPayment()

        context = {
            'post': post,
            'url' : url,
            'form' : form,

        }
        return render(request, 'ent/article_detail.html', context)


    def post(self, request, id, slug):
        post_increament = get_object_or_404(Stores, id=id, slug=slug)

        post_increament.view_count +=1
        post_increament.save()
        post = get_object_or_404(Post, id=id, slug=slug)
        url = f"https://yctmarket.pythonanywhere.com{post.image.url}"



        amount = int(str(post.amount) + "00")

        postTitle = post.title
        if 'email' in request.POST:
            form = EmailFormForPayment(request.POST or None)

            if form.is_valid():
                firstname = form.cleaned_data['firstname']
                print(firstname)
                lastname = form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                phoneNumber = form.cleaned_data['phoneNumber']
                print(phoneNumber)
                subject = f"Customer about to pay for your {post.title} product at yctmarket.com"
                message = '%s %s %s %s %s %s ' %(postTitle, firstname, lastname, email, address, phoneNumber)
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
                return redirect(checkout)
        else:
            form = EmailFormForMeetUp(request.POST or None)

            if form.is_valid():
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                phoneNumber = form.cleaned_data['phoneNumber']
                subject = f"A potential customer from yctmarket.com has interest in your {post.title} product"
                message = '%s %s %s %s %s %s ' %(postTitle, firstname, lastname, email, address, phoneNumber)
                emailFrom = [settings.EMAIL_HOST_USER]
                emailTo = post.author.email
                send_mail(subject, message, emailFrom, emailTo, fail_silently=True )


                subject1 = f"A potential customer from yctmarket.com has interest in the {post.title} product /n Custumer FirstName: {firstname} /n Customer LastName: {lastname} /n Customer Address: {address} /n Customer Number: {phoneNumber}"
                message2 = '%s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber)
                emailFrom2 = [settings.EMAIL_HOST_USER]
                emailTo2 = [settings.EMAIL_HOST_USER]
                send_mail(subject1, message2, emailFrom2, emailTo2, fail_silently=True )


        return redirect('thanks')






def article_detail(request, id, slug):
    post_increament = get_object_or_404(Post, id=id, slug=slug)
    post_increament.view_count +=1
    post_increament.save()
    post = get_object_or_404(Post, id=id, slug=slug, available=True)
    cart = Cart(request)
    #amount = post.amount
    #postTitle = post.title
    form = CartAddProductForm()

    context = {
         'post': post,
         'form' : form,
         'cart' : cart,

     }
    return render(request, 'ent/article_detail.html', context)

         #if form.is_valid():
         #    firstname = form.cleaned_data['firstname']
         #    lastname = form.cleaned_data['lastname']
         #    email = form.cleaned_data['email']
         #    address = form.cleaned_data['address']
         #    phoneNumber = form.cleaned_data['phoneNumber']
         #    subject = 'Customer about to pay at yctmarket'
         #    message = '%s %s %s %s %s ' %(firstname, lastname, email, address, phoneNumber)
         #    emailFrom = [settings.EMAIL_HOST_USER]
         #    emailTo = [settings.EMAIL_HOST_USER]
         #    send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

        #     r = PurchaseReference(firstname=firstname, lastname=lastname, email=email)
         #    reference = str(r.reference)
         #    r.save()

          #   headers = {
           #          'Authorization': 'Bearer sk_live_ffb5db8bf8d3abe7f343a743ae58ac5911c68d11',
        #             'Content-Type': 'application/json',
         #        }


         #    data = {"reference": reference, "amount": amount, "email": email}
         #    url = "https://api.paystack.co/transaction/initialize"
         #    response = requests.request("POST", url, headers=headers, json=data)
         #    res = response.json()

         #   checkout = res['data']['authorization_url']










def about(request):
    context = {}
    template = 'ent/about.html'
    return render(request,template,context)


def thank_you(request):
    context = {}
    template = 'ent/thank_you.html'
    return render(request,template,context)


def plan(request):
    context = {}
    template = 'ent/plan.html'
    return render(request,template,context)



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string("ent/activate.html",
                {
                    'user':user,
                    'domain':current_site.domain,
                    #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': generate_token.make_token(user)
                }

                )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.send()

            #messages.add_message(request, messages.SUCCESS, 'account created successfully')
            return render(request, "ent/confirm_email.html")
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, "ent/register.html", context)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            print('checking if the error is from the uid')
            print(uid)
            print("generating token")
            print(generate_token.check_token(user, token))
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        #user = None
        #except Exception as identifier:
            user = None
            print("failure to work")


        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, 'account activated successfully')
            return redirect('user_login')
        return render(request, "ent/activate_failed.html", status=401)



@login_required(login_url="user_login")
def upload_free_at_given(request):
    if request.method == 'POST':
        form = PostCreateFormForFree(request.POST, request.FILES)
        if form.is_valid():
            r = uuid.uuid4()
            reference = str(r)
            post = form.save(commit=False)
            post.author = request.user
            post.reference = reference
            post.save()
            messages.success(request, "Post has been successfully created.")
            return redirect('ent:article_list')
    else:
        form = PostCreateFormForFree()
    context = {
        'form': form,
    }
    return render(request, 'ent/upload_free_at_given.html', context)







@login_required(login_url="user_login")
def pay_per_upload(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            duration = form.cleaned_data['duration']

            #title = request.POST['title']
            #duration = int(request.POST['duration'])
            #category = request.POST['category']
            #amount = request.POST['amount']
            #description = request.POST['description']
            r = uuid.uuid4()
            reference = str(r)


            post = form.save(commit=False)
            post.author = request.user
            post.reference = reference
            post.save()
            #article = Article.objects.filter(reference=reference)
            #reference = str(article[0].reference)
            user1 = request.user
            user = User.objects.get(username=user1)
            email = user.email

            headers = {
                'Authorization': 'Bearer sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111',
                'Content-Type': 'application/json',
            }

            if duration == 7:
                price = 10000
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

            data = {"reference": reference, "amount":payment, "email":email}
            url = "https://api.paystack.co/transaction/initialize"
            response = requests.request("POST", url, headers=headers, json=data)

            #response = requests.post('https://api.paystack.co.transaction/initialize', headers=headers, json=data)
            res = response.json()
            print(res)

            checkout = res['data']['authorization_url']

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
                    messages.info(request, 'User not active, please login')
                    return HttpResponseRedirect(reverse('ent:article_list'))
            else:
                messages.error(request, 'Information provided not correct. Check username or password')
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