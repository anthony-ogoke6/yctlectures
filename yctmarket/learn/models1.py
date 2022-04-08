from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


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
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_created')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    amount  =       models.PositiveIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default.jpg')
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("ent:article_detail", args=[self.id, self.slug])



@receiver(pre_save, sender=Department)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug



class Course(models.Model):
    course = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'


    def __str__(self):
        return '{}. {}'.format(self.order, self.name)




class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    question = models.CharField(max_length=200, null=True, blank=True,)
    option1 = models.CharField(max_length=200, null=True, blank=True,)
    option2 = models.CharField(max_length=200, null=True, blank=True,)
    option3 = models.CharField(max_length=200, null=True, blank=True,)
    option4 = models.CharField(max_length=200, null=True, blank=True,)
    description = models.TextField(null=True, blank=True,)
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