from django import template


register = template.Library()


from ..models import Post
from django.contrib.auth.models import User


@register.simple_tag
def total_posts(user):
 return Post.published.filter(author=user).count()


@register.inclusion_tag('ent/posts_per_user.html')
def show_posts_per_user(user):
    user_posts = Post.published.filter(author=user).order_by('-created')
    print(user_posts)
    return {'user_posts': user_posts}