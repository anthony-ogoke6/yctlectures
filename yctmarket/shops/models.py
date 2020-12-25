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

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")




class Stores(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    DURATION_CHOICES = (
        (7,'1 Week'),
        (186, '6 Months'),
        (366,'1 Year'),

    )

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
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

    storename       =       models.CharField(max_length=200)
    description         =       models.TextField(default='')
    status              =       models.CharField(max_length=10, choices=BLANK_CHOICE_DASH + list(STATUS_CHOICES))
    slug                =       models.SlugField(max_length=200)
    #amount          =       models.PositiveIntegerField(default=0)
    category            =       models.CharField( max_length=100, choices=BLANK_CHOICE_DASH + list(CATEGORY_CHOICES))
    logo           =       models.ImageField(blank=True, null=True)
    tags                = TaggableManager()
    owner            =       models.OneToOneField(User, on_delete=models.CASCADE, related_name='store_owner_name')
    available           =       models.BooleanField(default=True)
    #stock               =       models.PositiveIntegerField(default=0)

    created             =       models.DateTimeField(auto_now_add=True)
    updated             =       models.DateTimeField(auto_now=True)
    published_date      =       models.DateTimeField(auto_now_add=True)
    view_count          =       models.PositiveIntegerField(default=0)
    duration            =       models.PositiveIntegerField(blank=True, null=True, choices=BLANK_CHOICE_DASH + list(DURATION_CHOICES))



    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.storename


    def get_absolute_url(self):
        return reverse("store_detail", args=[self.id, self.slug])




@receiver(pre_save, sender=Stores)
def pre_save_slug2(sender, **kwargs):
    slug = slugify(kwargs['instance'].storename)
    kwargs['instance'].slug = slug




class NamesOfPeopleWhoHaveOwnedShops(models.Model):
    name       =       models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)




class Shops(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    DURATION_CHOICES = (
        (7,'1 Week'),
        (186, '6 Months'),
        (366,'1 Year'),
    )

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
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

    storename       =       models.CharField(max_length=200)
    description         =       models.TextField(default='')
    status              =       models.CharField(max_length=10, choices=BLANK_CHOICE_DASH + list(STATUS_CHOICES))
    slug                =       models.SlugField(max_length=200)
    #amount          =       models.PositiveIntegerField(default=0)
    category            =       models.CharField( max_length=100, choices=BLANK_CHOICE_DASH + list(CATEGORY_CHOICES))
    logo                =       models.ImageField(blank=True, null=True)
    tags                = TaggableManager()
    owner            =       models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_owner_name')
    available           =       models.BooleanField(default=True)
    #stock               =       models.PositiveIntegerField(default=0)

    created             =       models.DateTimeField(auto_now_add=True)
    updated             =       models.DateTimeField(auto_now=True)
    view_count          =       models.PositiveIntegerField(default=0)
    duration            =       models.PositiveIntegerField(blank=True, null=True, choices=BLANK_CHOICE_DASH + list(DURATION_CHOICES))



    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.storename


    def get_absolute_url(self):
        return reverse("store_detail", args=[self.id, self.slug])

@receiver(pre_save, sender=Shops)
def pre_save_slug3(sender, **kwargs):
    slug = slugify(kwargs['instance'].storename)
    kwargs['instance'].slug = slug




class Product(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    DURATION_CHOICES = (
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
    author              =       models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_posts')
    store               =       models.ForeignKey(Stores, default='', on_delete=models.CASCADE, related_name='product_in_store')
    tags                = TaggableManager()
    amount              =       models.PositiveIntegerField(default='')
    #amountInDols              =       models.PositiveIntegerField(default='1')
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
        return reverse("shops:shop_detail", args=[self.id, self.slug])



@receiver(pre_save, sender=Product)
def pre_save_slug1(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug

