from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

#from ckeditor.fields import RichTextField


# Create your models here.




class PhoneNumber(models.Model):
	user            =      models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_number')
	phone_number    =      models.CharField(max_length=200)
	matric_number   =      models.CharField(max_length=15, default="0")

	class Meta:
		verbose_name = 'phone number'
		verbose_name_plural = 'phone numbers'

	def __str__(self):
		return self.user.username


class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
	    return reverse('ent:product_list_by_category', args=[self.slug])


@receiver(pre_save, sender=Category)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug




class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")



class Article(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    DURATION_CHOICES = (
        (7,'1 Week'),
        (14,'2 Weeks'),
        (28,'3 Weeks'),
        (31,'1 Month'),
        (366,'1 Year'),

    )

    CATEGORY_CHOICES = (
        ('Agriculture & Food','Agriculture & Food'),
        ('Animals & Pets','Animals & Pets'),
        ('Babies & Kids','Babies & Kids'),
        ('Commercial Equipment & Tool','Commercial Equipment & Tool'),
        ('Electronics','Electronics'),
        ('Fashion','Fashion'),
        ('Health & Beauty','Health & Beauty'),
        ('Home, Furniture & Appliances','Home, Furniture & Appliances'),
        ('Mobile Phones & Tablets','Mobile Phones & Tablets'),
        ('Property','Property'),
        ('Repair & Construction','Repair & Construction'),
        ('Seeking Work - CVs','Seeking Work - CVs'),
        ('Services','Services'),
        ('Sport, Art & Outdoors','Sport, Art & Outdoors'),
        ('Vehicles','Vehicles'),

    )

    reference           =       models.UUIDField( editable=False, unique=True)
    title               =       models.CharField(max_length=200)
    slug                =       models.SlugField(max_length=200)
    status              =       models.CharField(max_length=10, choices=BLANK_CHOICE_DASH + list(STATUS_CHOICES))

    author              =       models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    amount              =       models.PositiveIntegerField(default='')
    amountInDols              =       models.PositiveIntegerField(default='1')
    #category            =       models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products1')
    category            =       models.CharField( max_length=100, choices=BLANK_CHOICE_DASH + list(CATEGORY_CHOICES))
    description         =       models.TextField()
    video               =       models.FileField(blank=True, null=True)
    image               =       models.ImageField(blank=True, null=True)
    bodysnippet         =       models.TextField(default='', blank=True, null=True)
    body                =       RichTextUploadingField(default='', blank=True, null=True)
    link               =       models.TextField(blank=True, null=True)
    image2              =       models.ImageField(blank=True, null=True)
    image3              =       models.ImageField(blank=True, null=True)

    view_count          =       models.PositiveIntegerField(default=0)

    duration            =       models.PositiveIntegerField(blank=True, null=True, choices=BLANK_CHOICE_DASH + list(DURATION_CHOICES))
    available           =       models.BooleanField(default=True)
    stock               =       models.PositiveIntegerField(default=0)
    created             =       models.DateTimeField(auto_now_add=True)
    updated             =       models.DateTimeField(auto_now=True)



    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def snippet(self):
        return self.bodysnippet[:200] + "..."

    def total_likes(self):
        return self.likes.count()

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.image2.delete()
        self.image3.delete()
        super().delete(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("ent:article_detail", args=[self.id, self.slug])





@receiver(pre_save, sender=Article)
def pre_save_slug2(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug





class Post(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    DURATION_CHOICES = (
        (7,'1 Week'),
        (14,'2 Weeks'),
        (28,'3 Weeks'),
        (31,'1 Month'),
        (366,'1 Year'),

    )

    CATEGORY_CHOICES = (
        ('Agriculture & Food','Agriculture & Food'),
        ('Animals & Pets','Animals & Pets'),
        ('Babies & Kids','Babies & Kids'),
        ('Commercial Equipment & Tool','Commercial Equipment & Tool'),
        ('Electronics','Electronics'),
        ('Fashion','Fashion'),
        ('Health & Beauty','Health & Beauty'),
        ('Home, Furniture & Appliances','Home, Furniture & Appliances'),
        ('Mobile Phones & Tablets','Mobile Phones & Tablets'),
        ('Property','Property'),
        ('Repair & Construction','Repair & Construction'),
        ('Seeking Work - CVs','Seeking Work - CVs'),
        ('Services','Services'),
        ('Sport, Art & Outdoors','Sport, Art & Outdoors'),
        ('Vehicles','Vehicles'),
    )

    reference           =       models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title               =       models.CharField(max_length=200)
    slug                =       models.SlugField(max_length=200)
    status              =       models.CharField(max_length=10, choices=BLANK_CHOICE_DASH + list(STATUS_CHOICES))

    author              =       models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_posts')
    tags                = TaggableManager()
    amount              =       models.PositiveIntegerField(default='')
    amountInDols              =       models.PositiveIntegerField(default='1')
    #category            =       models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products2')
    category            =       models.CharField( max_length=100, choices=BLANK_CHOICE_DASH + list(CATEGORY_CHOICES))
    description         =       models.TextField()
    video               =       models.FileField(blank=True, null=True)
    image               =       models.ImageField(blank=True, null=True)
    bodysnippet         =       models.TextField(default='', blank=True, null=True)
    body                =       RichTextUploadingField(default='', blank=True, null=True)
    link               =       models.TextField(blank=True, null=True)
    image2              =       models.ImageField(blank=True, null=True)
    image3              =       models.ImageField(blank=True, null=True)
    view_count          =       models.PositiveIntegerField(default=0)

    duration            =       models.PositiveIntegerField(blank=True, null=True, choices=BLANK_CHOICE_DASH + list(DURATION_CHOICES))
    available           =       models.BooleanField(default=True)
    stock               =       models.PositiveIntegerField(default=0)

    created             =       models.DateTimeField(auto_now_add=True)
    updated             =       models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def snippet(self):
        return self.bodysnippet[:200] + "..."

    def total_likes(self):
        return self.likes.count()

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.image2.delete()
        self.image3.delete()
        super().delete(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("ent:article_detail", args=[self.id, self.slug])



@receiver(pre_save, sender=Post)
def pre_save_slug1(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug







class Stores(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    storename       =       models.CharField(max_length=200)
    description         =       models.TextField(default='')
    slug                =       models.SlugField(max_length=200)
    logo           =       models.ImageField(blank=True, null=True)
    owner            =       models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_name')


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.storename

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("ent:store_detail", args=[self.id, self.slug])




class AdvertImages(models.Model):

    DURATION_CHOICES = (
        (7,'1 Week'),
        (14,'2 Weeks'),
        (28,'3 Weeks'),
        (31,'1 Month'),
        (366,'1 Year'),

    )


    title               =       models.CharField(max_length=200)
    slug                =       models.SlugField(max_length=200)
    company_name    =       models.CharField(max_length=200)
    amount          =       models.PositiveIntegerField(default=0)
    #duration        =       models.CharField(max_length=10)
    description         =       models.TextField(default='')
    body            =       RichTextUploadingField(default='', blank=True, null=True)

    pic             =       models.ImageField(upload_to='images/', blank=True, null=True)
    vid             =       models.FileField(blank=True, null=True)

    pic2              =       models.ImageField(blank=True, null=True)
    pic3              =       models.ImageField(blank=True, null=True)
    pic4              =       models.ImageField(blank=True, null=True)
    link               =       models.TextField(blank=True, null=True)
    restrict_comment    =       models.BooleanField(default=False)
    view_count          =       models.PositiveIntegerField(default=0)

    created             =       models.DateTimeField(auto_now_add=True)
    updated             =       models.DateTimeField(auto_now=True)
    duration            =       models.PositiveIntegerField(blank=True, null=True, choices=BLANK_CHOICE_DASH + list(DURATION_CHOICES))


    def __str__(self):
        return str(self.company_name)

    class Meta:
        ordering = ['-id']



    def get_absolute_url(self):
        return reverse("ent:advert_detail", args=[self.id, self.slug, self.amount])



@receiver(pre_save, sender=AdvertImages)
def pre_save_slug4(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug




class Reference(models.Model):
    user_reference_number      =       models.CharField(max_length=200)



    def __str__(self):
        return str(self.reference)


class PurchaseReference(models.Model):
    firstname = models.CharField(max_length=100) # Note that Django suggests getting the User from the settings for relationship definitions
    lastname = models.CharField(max_length=100)
    reference = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=150,blank=True)
    #address = models.TextField(max_length=300)
    #phoneNumber = models.CharField(max_length=14, blank=False, null=False)


    def __str__(self):
        return str(self.reference)


class InfiniteScroll(models.Model):
    start = models.PositiveIntegerField(default=0) # Note that Django suggests getting the User from the settings for relationship definitions
    end = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.start)






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return "Profile of user {}".format(self.user.username)


class Images(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return str(self.post.id)


class Comment(models.Model):
    post = models.ForeignKey(AdvertImages, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post Title: \n{} \n \nComment by: {} \n'.format(self.post.title, str(self.user.username))

