from django import template

from voting.models import School, Department, Course, Content, Assignment, Score


register = template.Library()


from voting.models import Department
from django.contrib.auth.models import User


@register.simple_tag
def courses_students_is_in(user):
	qs = Department.objects.all()
	courses_students_is_in = None
	if user:
			courses_students_is_in = qs.filter(students__in=[user])
			print(user)
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







@register.simple_tag
def answered_assignment1(user, question, id, topic_id):
    course = Department.objects.get(id=id)
    module = course.modules1.get(id=topic_id)
    assignment = module.assignments1.get(id=question)
    print(assignment)
    print('assignment')
    score_questions = []
    score_answer = []
    score = Score.objects.filter(user=user, module=module, assignment=assignment)
    for i in score:
        score_questions.append(i.question)
        score_answer.append(i.student_answer)
    if assignment.option1 in score_answer:
        return True
    elif assignment.option2 in score_answer:
        return True
    elif assignment.option3 in score_answer:
        return True
    elif assignment.option4 in score_answer:
        return True
    elif assignment.option5 in score_answer:
        return True
    elif assignment.option6 in score_answer:
        return True
    elif assignment.option7 in score_answer:
        return True
    elif assignment.option8 in score_answer:
        return True
    elif assignment.option9 in score_answer:
        return True
    elif assignment.option10 in score_answer:
        return True
    elif assignment.option11 in score_answer:
        return True
    elif assignment.option12 in score_answer:
        return True
    elif assignment.option13 in score_answer:
        return True
    elif assignment.option14 in score_answer:
        return True
    elif assignment.option15 in score_answer:
        return True
    elif assignment.option16 in score_answer:
        return True
    else:
        return False




@register.simple_tag
def answered_assignment2(user, question, id, topic_id):
    course = Department.objects.get(id=id)
    module = course.modules1.get(id=topic_id)
    assignment = module.assignments1.get(id=question)
    print(assignment)
    score_questions = []
    score = Score.objects.filter(user=user, module=module, assignment=assignment)
    for i in score:
        score_questions.append(i.question)
    if assignment.question in score_questions:
        return True
    else:
        return False



