from django.contrib.auth.models import Group
from django import template




register = template.Library()



@register.filter(name='has_group')
def has_group(user, group_name):
    # try:
    #     group = Group.objects.get(name=group_name)
    # except Group.DoesNotExist:
    #     return False
    # return group in user.group.all()
    return user.groups.filter(name=group_name).exists()
