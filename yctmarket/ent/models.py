from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField

#from ckeditor.fields import RichTextField




class Departments(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'Department'
		verbose_name_plural = 'Departments'

	def __str__(self):
		return self.name



# Create your models here.
class PhoneNumber(models.Model):

    PREFIX_CHOICES = (
        ('Dr.','Dr.'),
        ('Prof.','Prof.'),
        ('Engr.','Engr.'),
        ('Mr.','Mr.'),
        ('Mrs.','Mrs.'),
        ('Miss.','Miss.'),
        )

    LEVEL = (
        ('ND1','ND1'),
        ('ND2','ND2'),
        ('ND3','ND3'),
        ('HND1','HND1'),
        ('HND2','HND2'),
        ('HND3','HND3'),
        ('100L','100L'),
        ('200L','200L'),
        ('300L','300L'),
        ('400L','400L'),
        )


    DEPARTMENT = (
        ('Accountancy','Accountancy'),
        ('Agricultural Technology','Agricultural Technology'),
        ('Agricultural and Bio-Environmental Engineering','Agricultural and Bio-Environmental Engineering'),
        ('Architecture','Architecture'),
        ('Art Education','Art Education'),
        ('Banking and Finance','Banking and Finance'),
        ('Biological Science','Biological Science'),
        ('Building Technology','Building Technology'),
        ('Business Administration','Business Administration'),
        ('Business Education','Business Education'),
        ('Chemical Engineering','Chemical Engineering'),
        ('Chemical Science','Chemical Science'),
        ('Civil Engineering','Civil Engineering'),
        ('Computer Engineering','Computer Engineering'),
        ('Computer Technology','Computer Technology'),
        ('Educational Foundation','Educational Foundation'),
        ('Electrical Electronics Engineering','Electrical Electronics Engineering'),
        ('Estate Management','Estate Management'),
        ('Fashion Design','Fashion Design'),
        ('Fine Art','Fine Art'),
        ('Food Technology','Food Technology'),
        ('Graphics Design','Graphics Design'),
        ('Hospitality Management Technology','Hospitality Management Technology'),
        ('Industrial Design','Industrial Design'),
        ('Industrial Maintenance Engineering','Industrial Maintenance Engineering'),
        ('Languages','Languages'),
        ('Leisure and Tourism','Leisure and Tourism'),
        ('Marine Engineering','Marine Engineering'),
        ('Marketing','Marketing'),
        ('Mass Communication','Mass Communication'),
        ('Mathematics','Mathematics'),
        ('Mechanical Engineering','Mechanical Engineering'),
        ('Mechatronics Engineering','Mechatronics Engineering'),
        ('Metallurgical Engineering','Metallurgical Engineering'),
        ('Mineral and Petroleum Resources Engineering','Mineral and Petroleum Resources Engineering'),
        ('Nutrition and Dietetics','Nutrition and Dietetics'),
        ('Office Technology Management','Office Technology Management'),
        ('Physical Science','Physical Science'),
        ('Polymer and Textile','Polymer and Textile'),
        ('Printing Technology','Printing Technology'),
        ('Public Administration','Public Administration'),
        ('Quantity Survey','Quantity Survey'),
        ('Science Laboratory Technology','Science Laboratory Technology'),
        ('Social Science','Social Science'),
        ('Statistics','Statistics'),
        ('Survey and Geoinfomatics','Survey and Geoinfomatics'),
        ('Technical Education','Technical Education'),
        ('Urban and Regional Planning','Urban and Regional Planning'),
        ('Vocational Education','Vocational Education'),
        ('Welding and Fabrication Engineering','Welding and Fabrication Engineering'),
        )

    user            =      models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_number')
    phone_number    =      models.CharField(max_length=200, blank=True, null=True)
    matric_number   =      models.CharField(max_length=200, blank=True, null=True)
    department   =      models.CharField(max_length=300, blank=True, null=True, choices=BLANK_CHOICE_DASH + list(DEPARTMENT))
    level          =      models.CharField(blank=True, null=True, max_length=10, choices=BLANK_CHOICE_DASH + list(LEVEL))
    prefix          =      models.CharField(blank=True, null=True, max_length=10, choices=BLANK_CHOICE_DASH + list(PREFIX_CHOICES))
    dob = models.DateField(default='2020-01-01', null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='images/', default='default.jpg')

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
        verbose_name = 'article'
        verbose_name_plural = 'articles'

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
    amount              =       models.PositiveIntegerField(default='')
    #category            =       models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products2')
    category            =       models.CharField( max_length=100, choices=BLANK_CHOICE_DASH + list(CATEGORY_CHOICES))
    description         =       models.TextField()
    video               =       models.FileField(blank=True, null=True)
    image               =       models.ImageField(upload_to='images/', blank=True, null=True, default='images/default1.jpng')
    bodysnippet         =       models.TextField(default='', blank=True, null=True)
    body                =       RichTextUploadingField(default='', blank=True, null=True)
    link               =       models.TextField(blank=True, null=True)
    image2              =       models.ImageField(upload_to='images/', blank=True, null=True, default='images/default1.png')
    image3              =       models.ImageField(upload_to='images/', blank=True, null=True, default='images/default1.png')
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






class Face(models.Model):
    objects = models.Manager()      #Our default Manager
    published = PublishedManager()  #Our Custom Model Manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    reference           =       models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title               =       models.CharField(max_length=200)
    slug                =       models.SlugField(max_length=200)
    status              =       models.CharField(max_length=10, choices=BLANK_CHOICE_DASH + list(STATUS_CHOICES))

    author              =       models.ForeignKey(User, on_delete=models.CASCADE, related_name='face_author')

    image               =       models.ImageField(blank=True, null=True)
    body                =       RichTextUploadingField(default='', blank=True, null=True)
    link               =       models.TextField(blank=True, null=True)
    view_count          =       models.PositiveIntegerField(default=0)

    created             =       models.DateTimeField(auto_now_add=True)
    updated             =       models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("ent:face_detail", args=[self.id, self.slug])



@receiver(pre_save, sender=Face)
def pre_save_slug8(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug




class AdvertImages(models.Model):

    DURATION_CHOICES = (
        (7,'1 Week'),
        (14,'2 Weeks'),
        (28,'3 Weeks'),
        (31,'1 Month'),
        (366,'1 Year'),

    )


    DEPARTMENT = (
        ('Accountancy','Accountancy'),
        ('Agricultural Technology','Agricultural Technology'),
        ('Agricultural and Bio-Environmental Engineering','Agricultural and Bio-Environmental Engineering'),
        ('Architecture','Architecture'),
        ('Art Education','Art Education'),
        ('Banking and Finance','Banking and Finance'),
        ('Biological Science','Biological Science'),
        ('Building Technology','Building Technology'),
        ('Business Administration','Business Administration'),
        ('Business Education','Business Education'),
        ('Chemical Engineering','Chemical Engineering'),
        ('Chemical Science','Chemical Science'),
        ('Civil Engineering','Civil Engineering'),
        ('Computer Engineering','Computer Engineering'),
        ('Computer Technology','Computer Technology'),
        ('Educational Foundation','Educational Foundation'),
        ('Electrical Electronics Engineering','Electrical Electronics Engineering'),
        ('Estate Management','Estate Management'),
        ('Fashion Design','Fashion Design'),
        ('Fine Art','Fine Art'),
        ('Food Technology','Food Technology'),
        ('Graphics Design','Graphics Design'),
        ('Hospitality Management Technology','Hospitality Management Technology'),
        ('Industrial Design','Industrial Design'),
        ('Industrial Maintenance Engineering','Industrial Maintenance Engineering'),
        ('Languages','Languages'),
        ('Leisure and Tourism','Leisure and Tourism'),
        ('Marine Engineering','Marine Engineering'),
        ('Marketing','Marketing'),
        ('Mass Communication','Mass Communication'),
        ('Mathematics','Mathematics'),
        ('Mechanical Engineering','Mechanical Engineering'),
        ('Mechatronics Engineering','Mechatronics Engineering'),
        ('Metallurgical Engineering','Metallurgical Engineering'),
        ('Mineral and Petroleum Resources Engineering','Mineral and Petroleum Resources Engineering'),
        ('Nutrition and Dietetics','Nutrition and Dietetics'),
        ('Office Technology Management','Office Technology Management'),
        ('Physical Science','Physical Science'),
        ('Polymer and Textile','Polymer and Textile'),
        ('Printing Technology','Printing Technology'),
        ('Public Administration','Public Administration'),
        ('Quantity Survey','Quantity Survey'),
        ('Science Laboratory Technology','Science Laboratory Technology'),
        ('Social Science','Social Science'),
        ('Statistics','Statistics'),
        ('Survey and Geoinfomatics','Survey and Geoinfomatics'),
        ('Technical Education','Technical Education'),
        ('Urban and Regional Planning','Urban and Regional Planning'),
        ('Vocational Education','Vocational Education'),
        ('Welding and Fabrication Engineering','Welding and Fabrication Engineering'),
        )


    LEVEL = (
        ('ND1','ND1'),
        ('ND2','ND2'),
        ('ND3','ND3'),
        ('HND1','HND1'),
        ('HND2','HND2'),
        ('HND3','HND3'),
        ('100L','100L'),
        ('200L','200L'),
        ('300L','300L'),
        ('400L','400L'),
        )

    title               =       models.CharField(max_length=200)
    slug                =       models.SlugField(max_length=200)
    company_name    =       models.CharField(max_length=200)
    amount          =       models.PositiveIntegerField(default=0)
    #duration        =       models.CharField(max_length=10)
    description         =       models.TextField(default='', blank=True, null=True)
    level          =      MultiSelectField(blank=True, null=True, choices=LEVEL)
    department          =      MultiSelectField(blank=True, null=True, choices=DEPARTMENT)
    #department              =       models.ManyToManyField(Departments, related_name='user_department', blank=True, null=True)
    body            =       RichTextUploadingField(default='')

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
        verbose_name = 'AdvertImage'
        verbose_name_plural = 'AdvertImages'



    def get_absolute_url(self):
        return reverse("ent:advert_detail", args=[self.id, self.slug, self.amount])



@receiver(pre_save, sender=AdvertImages)
def pre_save_slug4(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug







class DepartmentalAccessLevel(models.Model):
    name = models.CharField(max_length=800, null=True, blank=True)
    advert_images = models.ForeignKey(AdvertImages, null=True, blank=True, on_delete=models.CASCADE, related_name='email_level')
    class Meta:
        verbose_name = 'Email Level Notification'
        verbose_name_plural = 'Email Level Notification'

    def __str__(self):
        return self.name



@receiver(post_save, sender=AdvertImages)
def send_user_notification_email(sender, instance, created, **kwargs):

    # if a new officer is created, compose and send the email
    if created:
        email_list = []
        users = User.objects.all()
        try:
            level = instance.level
        except:
            level = None

        try:
            dept = instance.department
        except:
            dept = None

        if level != None:
            if dept != None:
                for i in users:
                    try:
                        user_level = i.user_number.all()[0].level
                    except:
                        user_level = None

                    try:
                        user_dept = i.user_number.all()[0].department
                    except:
                        user_dept = None

                    if user_level != None:
                        if user_dept != None:
                            if user_level in level:
                                if user_dept in dept:
                                    email = i.email
                                    if email in email_list:
                                        pass
                                    else:
                                        email_list.append(email)
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
            else:
                for i in users:
                    try:
                        user_level = i.user_number.all()[0].level
                    except:
                        user_level = None

                    if user_level != None:
                        if user_level in level:
                            email = i.email
                            if email in email_list:
                                pass
                            else:
                                email_list.append(email)
                        else:
                            pass
                    else:
                        pass

        else:
            pass

        email_list.append(settings.EMAIL_HOST_USER)
        print(email_list)

        messge_content = f"{instance.title.upper()}: \nhttps://www.allschoolsng.com{instance.get_absolute_url()}"
        subject = "Allschoolsng Update"
        message = '%s' %(messge_content)
        emailFrom = [settings.EMAIL_HOST_USER]
        emailTo = email_list
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True )




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



class DonationReference(models.Model):
    firstname = models.CharField(max_length=100) # Note that Django suggests getting the User from the settings for relationship definitions
    lastname = models.CharField(max_length=100)
    amount =    models.PositiveIntegerField(default=0)
    reference = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=14, blank=False, null=False)


    def __str__(self):
        return str(self.reference)


class InfiniteScroll(models.Model):
    start = models.PositiveIntegerField(default=0) # Note that Django suggests getting the User from the settings for relationship definitions
    end = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.start)






class Profile(models.Model):
    PREFIX_CHOICES = (
        ('Dr.','Dr.'),
        ('Prof.','Prof.'),
        ('Engr.','Engr.'),
        ('Mr.','Mr.'),
        ('Mrs.','Mrs.'),
        ('Miss.','Miss.'),
        )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number    =      models.CharField(max_length=200, blank=True, null=True)
    matric_number   =      models.CharField(max_length=200, blank=True, null=True)
    department   =      models.CharField(max_length=15, blank=True, null=True)
    prefix          =      models.CharField(blank=True, null=True, max_length=10, choices=BLANK_CHOICE_DASH + list(PREFIX_CHOICES))
    dob = models.DateField(default='2020-01-01', null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='images/', default='default.jpg')
    def __str__(self):
        return "{} Profile".format(self.user.username)





@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Images(models.Model):
    #post = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', blank=True, null=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'



class Comment(models.Model):
    post = models.ForeignKey(AdvertImages, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post Title: \n{} \n \nComment by: {} \n'.format(self.post.title, str(self.user.username))

