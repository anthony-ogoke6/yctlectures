from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from ent.models import PurchaseReference
from django.core.mail import send_mail, EmailMessage
import json
import requests
from django.contrib import messages
from django.conf import settings

from braces.views import LoginRequiredMixin
from learn.models import Department, Assignment, Course, Content, Score
from .forms import CourseEnrollForm
from ent.models import PurchaseReference, PhoneNumber

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags









class StudentRegistrationView(CreateView):
	template_name = 'students/registration.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('students:student_course_list')
	def form_valid(self, form):
		result = super(StudentRegistrationView, self).form_valid(form)
		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password1'])
		login(self.request, user)
		return result


class StudentDepartmentDetailView(LoginRequiredMixin, DetailView):
	model = Department
	template_name = 'learn/detail.html'

	def get_queryset(self):
		qs = super(StudentDepartmentDetailView, self).get_queryset()
		return qs.filter(students__in=[self.request.user])

	def get_context_data(self, **kwargs):
		context = super(StudentDepartmentDetailView, self).get_context_data(**kwargs)
		# get course object
		department = self.get_object()
		if 'topic_id' in self.kwargs:
		# get current module
			context['topic'] = department.modules.get(id=self.kwargs['topic_id'])
			context['object_id'] = department.id
			context['object_slug'] = department.slug
			context['module_id'] = self.kwargs['topic_id']
		else:
			# get first module
			context['topic'] = department.modules.all()[0]
			context['object_id'] = department.id
			context['object_slug'] = department.slug
			context['module_id'] = department.modules.all()[0].id
		return context










class StudentEnrollCourseView(LoginRequiredMixin, FormView):
	department = None
	form_class = CourseEnrollForm
	def form_valid(self, form):
		self.department = form.cleaned_data['department']
		self.department.students.add(self.request.user)
		return super(StudentEnrollCourseView, self).form_valid(form)


	def get_success_url(self):
		return reverse_lazy('students:student_department_detail', args=[self.department.id])




class StudentDepartmentListView(LoginRequiredMixin, ListView):
	model = Department
	# template_name = 'students/list.html'
	template_name = 'learn/list1.html'

	def get_queryset(self):
		qs = super(StudentDepartmentListView, self).get_queryset()
		return qs.filter(students__in=[self.request.user])







def pay_for_course(request, id, slug):
	user = User.objects.get(username=request.user)
	firstname = user.first_name
	lastname = user.last_name
	email = user.email
	brand = "Department"
	course = get_object_or_404(Department, id=id, slug=slug)
	course_name = course.name
	course_slug = course.name
	amount = int(str(course.amount) + "00")
	print(amount)
	r = PurchaseReference(firstname=firstname, lastname=lastname, email=email)
	reference = str(r.reference)
	r.save()

	subject = f"Customer about to subscribe for {course_name} yctmarket"
	message = '%s %s %s ' %(firstname, lastname, email)
	emailFrom = [settings.EMAIL_HOST_USER]
	emailTo = [settings.EMAIL_HOST_USER]
	send_mail(subject, message, emailFrom, emailTo, fail_silently=True )

	headers = {
	        'Authorization': 'Bearer sk_live_ffb5db8bf8d3abe7f343a743ae58ac5911c68d11',
	        'Content-Type': 'application/json',
	    }


	data = {"reference": reference, "amount": amount, "email": email}
	url = "https://api.paystack.co/transaction/initialize"
	response = requests.request("POST", url, headers=headers, json=data)
	res = response.json()

	checkout = res['data']['authorization_url']
	return redirect(checkout)


def assignment(request, id, slug, topic_id):
	user = User.objects.get(username=request.user)
	course = Department.objects.get(id=id, slug=slug)
	module = course.modules.get(id=topic_id)
	assignment = module.assignments.all()
	paginator = Paginator(assignment, 1)
	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)

	subject = f"Student about to subscribe for Course:{course.name} In Module:{module.name} yctmarket"
	message = '%s %s %s ' %(user.first_name, user.last_name, user.email)
	emailFrom = [settings.EMAIL_HOST_USER]
	emailTo = [settings.EMAIL_HOST_USER]
	send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
	context = {
        'assignment': assignment,
        'questions': questions,
        'id': id,
        'slug': slug,
        'topic_id': topic_id,

    }
    # html = render_to_string('students/assignment.html', context, request=request)
    # return JsonResponse({'form': html})

	return render(request, 'learn/assignment.html', context)


def grade(request):
	user = User.objects.get(username=request.user)
	course = Department.objects.get(id=id, slug=slug)
	module = course.modules.get(id=topic_id)
	assignment = module.assignments.all()

	subject = f"Student about to subscribe for Course:{course.name} In Module:{module.name} yctmarket"
	message = '%s %s %s ' %(user.first_name, user.last_name, user.email)
	emailFrom = [settings.EMAIL_HOST_USER]
	emailTo = [settings.EMAIL_HOST_USER]
	send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
	context = {
        'assignment': assignment,
    }
    # html = render_to_string('students/assignment.html', context, request=request)
    # return JsonResponse({'form': html})

	return render(request, 'learn/assignment.html', context)

def saveans1(request, id, slug, topic_id, page_no):
	print(slug)
	print(page_no)
	page_no1 = int(page_no) - 1

	user = User.objects.get(username=request.user)
	phone = PhoneNumber.objects.get(user=user)
	matric_number  = phone.matric_number
	course = Department.objects.get(id=id, slug=slug)
	module = course.modules.get(id=topic_id)
	modules = course.modules.all()
	assignment = module.assignments.all()[page_no1]
	question = assignment.question
	correct_answer = assignment.answer
	score_grade = Score.objects.filter(question=question)
	student_taken_assignment = []

	if request.is_ajax and request.method == 'POST':
		ans = request.POST['ans']
		print('ans')
		print(ans)
		student_answer = ans
		for i in score_grade:
			student_taken_assignment.append(i.user)
		if user in student_taken_assignment:
			return render(request, 'learn/grade.html', {'msg':'Already submitted answer'})
		else:
			if str(student_answer) == str(correct_answer):
				grade = 1
				score = Score(user=user,
					course=course,
					module=module,
					assignment=assignment,
					question=question,
					correct_answer=correct_answer,
					student_answer=student_answer,
					score=grade)
				score.save()
				total = 0
			else:
				grade = 0
				score = Score(user=user,
					course=course,
					module=module,
					assignment=assignment,
					question=question,
					correct_answer=correct_answer,
					student_answer=student_answer,
					score=grade)
				score.save()
				total = 0
	else:
		grade = []
		scores = Score.objects.filter(user=user, course=course)
		instructor_email = course.instructor.email
		for i in scores:
			grade.append(i.score)
			#i.module.name


		total = sum(grade)


	context = {
	'total': total,
        #'name' : user.first_name,
        'user' : user,
        'matric_number' : matric_number,
        'course' : course,
        'module' : module,
        'modules' : modules,
        'assignment' : assignment,
        'scores' : scores,
    }

	html = render_to_string('learn/email_template.html', context, request=request)
	text_content = strip_tags(html)
	email = EmailMultiAlternatives(
		#subject

		f"Yabatech Student Grading",
		#content
		text_content,
		#from email
		settings.EMAIL_HOST_USER,
		#rec list
		[settings.EMAIL_HOST_USER]
		)
	email.attach_alternative(html, "text/html")
	email.send()
	# student_department_list
	return redirect('students:student_department_list')
	#return render(request, 'learn/grade.html', context)


def saveans(request):
	if request.is_ajax and request.method == 'POST':
		ans = request.POST['ans']
		print('ans')
		print(ans)
	# user = User.objects.get(username=request.user)
	# course = Department.objects.get(id=id, slug=slug)
	# module = course.modules.get(id=topic_id)
	# assignment = module.assignments.all()

	# subject = f"Student about to subscribe for Course:{course.name} In Module:{module.name} yctmarket"
	# message = '%s %s %s ' %(user.first_name, user.last_name, user.email)
	# emailFrom = [settings.EMAIL_HOST_USER]
	# emailTo = [settings.EMAIL_HOST_USER]
	# send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
	# context = {
 #        'assignment': assignment,
 #    }
    # html = render_to_string('students/assignment.html', context, request=request)
    # return JsonResponse({'form': html})

	# return render(request, 'learn/assignment.html', context)
	return render(request, 'learn/assignment.html')



class StudentAssesmentDetailView(LoginRequiredMixin, DetailView):
	model = Course
	template_name = 'students/assignment.html'

	def get_queryset(self):
		qs = super(StudentAssesmentDetailView, self).get_queryset()
		return qs.filter(students__in=[self.request.user])

	def get_context_data(self, **kwargs):
		context = super(StudentAssesmentDetailView, self).get_context_data(**kwargs)
		# get course object
		course = self.get_object()
		if 'topic_id' in self.kwargs:
		# get current module
			content = course.contents.get(id=self.kwargs['topic_id'])
			assesments = content.assesments.all()
		else:
			# get first module
			context['topic'] = department.modules.all()[0]
		return context