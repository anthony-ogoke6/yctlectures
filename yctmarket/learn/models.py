from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

from django.urls import reverse


from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.db.models.fields import BLANK_CHOICE_DASH
from multiselectfield import MultiSelectField

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField




# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name


@receiver(pre_save, sender=School)
def pre_save_slug1(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug






class Department(models.Model):


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



    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses')
    department_access_course = models.CharField(max_length=800, null=True, blank=True,)
    department_access = models.CharField(max_length=300, blank=True, null=True, choices=DEPARTMENT)
    level          =      models.CharField(blank=True, null=True, max_length=10, choices=LEVEL)
    name = models.CharField(max_length=200)
    amount  =       models.PositiveIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default.jpg')
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    general = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)
    overview = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("students:student_department_detail", args=[self.pk])



class DepartmentalAccess(models.Model):
    name = models.CharField(max_length=800, null=True, blank=True)
    course = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE, related_name='Department_courses')

    class Meta:
        verbose_name = 'Departmental Access'
        verbose_name_plural = 'Departmental Access'

    def __str__(self):
        return self.name


class DepartmentalAccessLevel(models.Model):
    name = models.CharField(max_length=800, null=True, blank=True)
    course = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE, related_name='Department_level')
    class Meta:
        verbose_name = 'Departmental Level Access'
        verbose_name_plural = 'Departmental Level Access'

    def __str__(self):
        return self.name






@receiver(pre_save, sender=Department)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug



class Course(models.Model):
    course = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=200)
    description = RichTextUploadingField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'


    def __str__(self):
        return '{}. {}'.format(self.order, self.name)




class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    question = models.CharField(max_length=200, null=True, blank=True,)
    option1 = models.CharField(max_length=200, null=True, blank=True,)
    option2 = models.CharField(max_length=200, null=True, blank=True,)
    option3 = models.CharField(max_length=200, null=True, blank=True,)
    option4 = models.CharField(max_length=200, null=True, blank=True,)
    show_question = models.BooleanField(default=False)
    #description = RichTextUploadingField(null=True, blank=True,)
    answer = models.CharField(max_length=200, null=True, blank=True,)

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'



class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_assignment')
    course = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='score_department')
    module = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='score_course')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='score_assignments')
    question = models.CharField(max_length=200, null=True, blank=True,)
    student_answer = models.CharField(max_length=200, null=True, blank=True,)
    correct_answer = models.CharField(max_length=200, null=True, blank=True,)
    score =   models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Score'
        verbose_name_plural = 'Scores'







class Content(models.Model):
    topic = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['topic'])

    class Meta:
        ordering = ['order']
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'



class ItemBase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_related')
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


    def render(self):
        return render_to_string('learn/content/{}.html'.format(self._meta.model_name), {'item': self})

    def __str__(self):
        return self.name

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()




class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentors')
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Course: \n{} \n \nComment by: {} \n'.format(self.course.name, str(self.user.username))