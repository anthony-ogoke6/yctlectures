from django.db import models
from django.contrib.auth.models import User
from learn.models import Department
import uuid

# Create your models here.
class PurchaseReference(models.Model):
    firstname = models.CharField(max_length=100, null=True, blank=True,) # Note that Django suggests getting the User from the settings for relationship definitions
    lastname = models.CharField(max_length=100, null=True, blank=True,)
    reference = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=150,null=True, blank=True,)
    brand = models.CharField(max_length=100, null=True, blank=True,)
    amount =    models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='student_subscribed_course')
    user  =       models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_payment', null=True, blank=True,)

    def __str__(self):
        return str(self.reference)
