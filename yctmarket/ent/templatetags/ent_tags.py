from django import template

from learn.models import Department, Score

from django.contrib.auth.models import User


register = template.Library()


from ..models import Post


@register.simple_tag
def total_posts(user):
 return Post.published.filter(author=user).count()


@register.inclusion_tag('ent/posts_per_user.html')
def show_posts_per_user(user):
    user_posts = Post.published.filter(author=user).order_by('-created')
    print(user_posts)
    return {'user_posts': user_posts}



@register.simple_tag
def courses_students_is_in(user):
	qs = Department.objects.all()
	courses_students_is_in = None
	if user:
			courses_students_is_in = qs.filter(students__in=[user])
	return courses_students_is_in




@register.simple_tag
def answered_assignment(user, id, slug):
    user = User.objects.get(username=user)
    course = Department.objects.get(id=id, slug=slug)
    modules = course.modules.all()
    chapters_that_student_have_attempted = []
    for i in modules:
    	if len(i.assignments.all()) > 0:
    		assignments = i.assignments.all()
    		for t in assignments:
    			question = t.question
    			scoring = Score.objects.filter(user=user, course=course, question=question)
    			if len(scoring) > 0:
    				order = int(i.order) + 1
    				print(order)
    				chapters_that_student_have_attempted.append(order)
    return chapters_that_student_have_attempted
