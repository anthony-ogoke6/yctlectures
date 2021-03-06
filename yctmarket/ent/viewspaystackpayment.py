
from .forms import *
from .forms import EmailFormForMeetUp, EmailFormForPayment, InfiniteScrollForm, PostCreateForm, PostCreateFormForFree, UserLoginForm, UserRegistrationForm, ReRequestActivationForm, CommentForm, ProfileForm, UserEditForm, ProfileEditForm
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
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from .models import Article, Profile, Reference, Post, AdvertImages, PurchaseReference, PhoneNumber, Images, Comment
import datetime
from taggit.models import Tag
from django.db.models import Count
import hmac
import hashlib
import json

import logging

logger = logging.getLogger(__name__)


def processPaystackWebhook(request):
    # paystack_sk = "sk_liveffb5db8bf8d3abe7f343a743ae58ac5911c68d11"
    '''
    The function takes an http request object containing the json data
    from paystack webhook client. Django's http request and response
    object was used for this example



    '''


    subject = "webhook has entered"
    msg = "hopefully webhook works"
    message = '%s ' %(msg)
    emailFrom = [settings.EMAIL_HOST_USER]
    emailTo = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, emailFrom, emailTo, fail_silently=True )



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
                        subject = "webhook from paystack via yctmarket"
                        message = '%s %s %s ' %(article.reference, title, author)
                        emailFrom = [settings.EMAIL_HOST_USER]
                        emailTo = [settings.EMAIL_HOST_USER]
                        send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
                        return HttpResponse(status=200)

    return HttpResponse(status=400)


def my_webhook_view(request):
    json_body = json.loads(request.body)
    print("webhook is working")

    subject = "webhook has entered"
    msg = "hopefully webhook works"
    message = '%s ' %(msg)
    emailFrom = [settings.EMAIL_HOST_USER]
    emailTo = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, emailFrom, emailTo, fail_silently=True )


    status = json_body['data']['status']
    if status == "success":
        reference = json_body['data']['reference']
        user_reference = Reference(user_reference_number=reference)
        user_reference.save()
        articles = Article.published.all()
        for article in articles:
            if article.reference == reference:
                title = article.title
                slug = article.slug
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

                post = Post(title=title, slug=slug, status=status, author=author, amount=amount, category=category, description=description, video=video, image=image, bodysnppet=bodysnippet, body=body, image2=image2, image3=image3, view_count=view_count, duration=duration, created=created, updated=updated)
                post.save()
                subject = "webhook from paystack via yctmarket"
                message = '%s %s %s ' %(article.reference, title, author)
                emailFrom = [settings.EMAIL_HOST_USER]
                emailTo = [settings.EMAIL_HOST_USER]
                send_mail(subject, message, emailFrom, emailTo, fail_silently=True )


                return HttpResponse(status=200)
        return HttpResponse(status=400)








def article_list(request, tag_slug=None):
    #pics =  AdvertImages.objects.all()
    #pic = Images.objects.all()

    articles = []


    posts = Post.published.all()

    news_search = request.GET.get('search')

    query = request.GET.get('q')
    #search_query = query.split()
    #if len(query)>=1:
        #for word in query:
    if query:
        posts = Post.published.filter(
            Q(title__icontains=query)|
            Q(category__icontains=query)|
            Q(tags__name__icontains=query)).distinct()

                #posts= Post.published.filter(lookups, is_active=True).distinct()
    ads = AdvertImages.objects.all()
    a = ads[0]
    b = ads[1]
    c = ads[2]
    d = ads[3]
    e = ads[4]
    f = ads[5]
    g = ads[6]
    h = ads[7]
    i = ads[8]
    j = ads[9]
    if news_search:
        ads = AdvertImages.objects.filter(
            Q(title__icontains=news_search)|
            Q(body__icontains=news_search)|
            Q(company_name__icontains=news_search)).distinct()




    #tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.published.filter(tags__in=[tag])






    #empty dict
    #data = []

    #data = []

    #querry all post in Post model


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


    if news_search:

        if len(ads) == 1:
            a = ads[0]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            }

        elif len(ads) == 2:
            b = ads[1]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            'b': b,
            }

        elif len(ads) == 3:
            c = ads[2]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            'b': b,
            'c': c,
            }

        elif len(ads) == 4:
            d = ads[3]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            }

        elif len(ads) == 5:
            e = ads[4]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'e': e,
            }

        elif len(ads) == 6:
            f = ads[5]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'e': e,
            'f': f,
            }

        elif len(ads) == 7:
            g = ads[6]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'e': e,
            'f': f,
            'g': g,
            }

        elif len(ads) == 8:
            h = ads[7]
            context = {
            'article': article,
            'news_search':news_search,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'e': e,
            'f': f,
            'g': g,
            'h': h,
            }
        elif len(ads) == 9:
            i = ads[8]
            context = {
                'article':article,
                'news_search':news_search,
                'a':a,
                'b':b,
                'c':c,
                'd':d,
                'e':e,
                'f':f,
                'g':g,
                'h':h,
                'i':i,
                }
        elif len(ads) == 10:
            context = {
                'article':article,
                'news_search':news_search,
                'a':a,
                'b':b,
                'c':c,
                'd':d,
                'e':e,
                'f':f,
                'g':g,
                'h':h,
                'i':i,
                'j':j,
                }



    else:
        context = {
        'article': article,
        #'content': content,
        #'pics': pics,
        #'pic': pic,
        'query': query,
        'news_search':news_search,
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'e': e,
        'f': f,
        'g': g,
        'h': h,
        'i':i,
        'j':j,
        }

    return render(request, 'ent/article_list.html', context)



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

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
     .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
     .order_by('-same_tags','-created')[:3]



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
        'similar_posts': similar_posts
    }

    return render(request, 'ent/article_detail.html', context)


def advert_details(request, id, slug, amount):
    post_increament = get_object_or_404(AdvertImages, id=id, slug=slug, amount=amount)

    post_increament.view_count +=1
    post_increament.save()
    related = []
    post = get_object_or_404(AdvertImages, id=id, slug=slug, amount=amount)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
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


    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None

            #messge_content = f"Post Title: {post.title} \n Comment by: {request.user} \n \n \nComment Content: \n{content}"
            #subject = "New comment from yctmarket.com"
            #message = '%s' %(messge_content)

            #emailFrom = [settings.EMAIL_HOST_USER]
            #emailTo = [settings.EMAIL_HOST_USER]
            #send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
                #subject = 'Comments reply from yctmarket'
                #message = '%s %s ' %(comment_qs, content,)
                #emailFrom = [settings.EMAIL_HOST_USER]
                #emailTo = [settings.EMAIL_HOST_USER]
                #send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()




        comments1 = Comment.objects.filter(post=post, reply=None).order_by('-id')
        email_list = []
        if comments1:
            for comment in comments1:
                email = comment.user.email

                if email in email_list:
                    pass
                else:
                    email_list.append(email)

        email_list.append(settings.EMAIL_HOST_USER)

        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            email_msg = []
            for email in email_list:
                if str(email) == str(request.user.email):
                    pass
                else:
                    email_msg.append(email)
            if reply_id:
                reply_email = []
                comment_qs = Comment.objects.get(id=reply_id)
                email_owner_comment = comment_qs.user.email
                for reply in comment_qs.replies.all():
                    user_email = reply.user.email
                    if user_email in reply_email:
                        pass
                    else:
                        reply_email.append(user_email)
                    if email_owner_comment in reply_email:
                        pass
                    else:
                        reply_email.append(email_owner_comment)
                        print(reply_email)

                reply_email_list = []
                for mail in reply_email:
                    if str(mail) == str(request.user.email):
                        pass
                    else:
                        reply_email_list.append(mail)

                reply_email_list.append(settings.EMAIL_HOST_USER)


                subject = 'Comments reply from www.yctmarket.com'
                message = '%s %s' %(comment_qs, f"\nreply by: {request.user.username} \n \nContent: \n{content} \n \n \nhttps://www.yctmarket.com{post.get_absolute_url()}",)
                print("look here")
                print(reply_email_list)
                emailFrom = [settings.EMAIL_HOST_USER]
                emailTo = reply_email_list
                send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
            else:
                messge_content = f"Post Title: \n{post.title} \n \nComment by: {request.user} \n \nContent: \n{content} \n \n \nhttps://www.yctmarket.com{post.get_absolute_url()}"
                subject = "New comment from yctmarket.com"
                message = '%s' %(messge_content)
                emailFrom = [settings.EMAIL_HOST_USER]
                emailTo = email_msg
                send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

    else:
        comment_form= CommentForm()


    context = {
        'post': post,
        'url' : url,
        'related':related,
        'comments': comments,
        'comment_form': comment_form,
    }
    if request.is_ajax():
        html = render_to_string('ent/comments.html', context, request=request)
        return JsonResponse({'form': html})

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
        form = UserCreationForm(request.POST, request.FILES)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            email = form.cleaned_data['email']
            dob = request.POST['dob']
            photo = request.POST['photo']
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phoneNumber']
            matric_number = form.cleaned_data['matric_number']
            password = form.cleaned_data['password1']
            new_user.set_password(form.cleaned_data['password1'])
            #new_user.is_active=False
            new_user.save()
            saved_user = User.objects.get(username=username)
            user_phone = PhoneNumber(user=saved_user, phone_number=phone_number, matric_number=matric_number)
            user_phone.save()
            Profile.objects.create(user=new_user, dob=dob, photo=photo)
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
        profile_form = ProfileForm()
    context = {
        'form': form,
        'profile_form': profile_form,
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
            post.body = request.POST['description']
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





@login_required(login_url="user_login")
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
            #number = request.user.phoneNumber
            #user_number = PhoneNumber.objects.get(user=request.user)
            #number = user_number.phone_number
            print(name)
            #print(number)

            headers = {
                'Authorization': 'Bearer sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111',
                'Content-Type': 'application/json',
            }

            if duration == 7:
                price = 50000
            elif duration == 14:
                price = 100000
            elif duration == 21:
                price = 150000
            elif duration == 28:
                price = 2000000
            elif duration == 31:
                price = 3000000
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
            if '@' in username:
                user =  User.objects.get(email=username)
                username = user.username
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




@login_required
def edit(request):
    username = request.user
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    print('first print')
    print(profile.photo)
    user_posts = Post.objects.filter(author=username)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            #profile_form.save(commit=False)
            #user_form.save(commit=False)
            print("up")
            #print(prof.cleaned_data['photo'])
            profile.photo = request.POST['photo']
            print("down")
            print(profile.photo)
            #prof.photo = profile_form.cleaned_data['photo']
            profile.dob = request.POST['dob']
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            profile.save()
            user.save()
            #prof = Profile.objects.get(user=user)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'ent/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'user_posts':user_posts, 'profile':profile})






def user_logout(request):
    logout(request)
    return redirect('ent:article_list')



def teacher(request):
    #collect id number
    return None


def student(request):
    #collect matric number
    return None

def post_delete(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    if request.user != post.author:
        raise Http404()
    post.delete()
    messages.warning(request, 'Post has been successfully deleted')
    return redirect('ent:article_list')