from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from ent.models import PurchaseReference
from django.core.mail import send_mail, EmailMessage
import json
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings

from braces.views import LoginRequiredMixin
from ent.forms import CommentForm

from voting.models import Department, Assignment, Course, Content, Score, Comment
from .forms import CourseEnrollForm
from ent.models import PurchaseReference, PhoneNumber

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags



from students1.models import PurchaseReference


from django.db.models import Sum



# import vimeo

# client = vimeo.VimeoClient(
#   token='{3acf0a01a68a09126a070e72946ae741}',
#   key='{3995db9d7d43af1fb2a82643223f06248c99ce1f}',
#   secret='{OLe5HrAF3hfSXG38foIv3whkGMVb0n5IqroU1LbbuFLVrLRNUWrdaBqSf4mJvMth5Y8zpL90hd2myx+3E8tgj2UJ4PdIclzn9XMUPR/67oM+6W/XidoS1Ka2OjRMvwLO}'
# )

# response = client.get(uri)
# print response.json()



# client.patch(uri, data={
#   'privacy': {
#     'view': 'disable†'
#   },
#   'password': 'helloworld'
# })

# print '%s will now require a password to be viewed on Vimeo.' % uri









class StudentRegistrationView(CreateView):
	template_name = 'students1/registration.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('students1:student_course_list')
	def form_valid(self, form):
		result = super(StudentRegistrationView, self).form_valid(form)
		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password1'])
		login(self.request, user)
		return result



# class StudentDepartmentDetailView(LoginRequiredMixin, DetailView):
# 	model = Department
# 	template_name = 'voting/detail.html'

# 	def get_queryset(self):
# 		qs = super(StudentDepartmentDetailView, self).get_queryset()
# 		return qs.filter(students__in=[self.request.user])

# 	def get_context_data(self, **kwargs):
# 		context = super(StudentDepartmentDetailView, self).get_context_data(**kwargs)
# 		# get course object
# 		department = self.get_object()
# 		if 'topic_id' in self.kwargs:
# 		# get current module
# 			context['topic'] = department.modules.get(id=self.kwargs['topic_id'])
# 			context['object_id'] = department.id
# 			context['object_slug'] = department.slug
# 			context['module_id'] = self.kwargs['topic_id']
# 		else:
# 			# get first module
# 			context['topic'] = department.modules.all()[0]
# 			context['object_id'] = department.id
# 			context['object_slug'] = department.slug
# 			context['module_id'] = department.modules.all()[0].id
# 		return context




class StudentDepartmentDetailView(LoginRequiredMixin, DetailView):
	model = Department
	template_name = 'voting/detail.html'




	def get_queryset(self):
		qs = super(StudentDepartmentDetailView, self).get_queryset()
		return qs.filter(students__in=[self.request.user])


	def get_context_data(self, **kwargs):
		context = super(StudentDepartmentDetailView, self).get_context_data(**kwargs)
		# get course object
		department = self.get_object()
		if 'topic_id' in self.kwargs:
		# get current module
			context['topic'] = department.modules1.get(id=self.kwargs['topic_id'])
			context['object_id'] = department.id
			context['object_slug'] = department.slug
			context['module_id'] = self.kwargs['topic_id']
		else:
			# get first module
			context['topic'] = department.modules1.all()[0]
			context['object_id'] = department.id
			context['object_slug'] = department.slug
			context['module_id'] = department.modules1.all()[0].id
		return context


	def get(self, request, *args, **kwargs):
		department = self.get_object()
		course = Department.objects.get(id=department.id, slug=department.slug)
		p = course

		if 'topic_id' in self.kwargs:

			module = course.modules1.get(id=self.kwargs['topic_id'])
			comments = Comment.objects.filter(course=module, reply=None).order_by('-id')
		else:
		    if department.modules1.all().count() > 0:
		        module = course.modules1.get(id=department.modules1.all()[0].id)
		        comments = Comment.objects.filter(course=module, reply=None).order_by('-id')
		    else:
		        module = None
		        comments = None




		comment_form= CommentForm()

		if 'topic_id' in self.kwargs:
		# get current module
			topic = department.modules1.get(id=self.kwargs['topic_id'])
			object_id = department.id
			object_slug = department.slug
			module_id = self.kwargs['topic_id']
		elif department.modules1.all().count() > 0:
		    topic = department.modules1.all()[0]
		    object_id = department.id
		    object_slug = department.slug
		    module_id = department.modules1.all()[0].id
		else:
		    topic = None
		    object_id = None
		    object_slug = None
		    module_id = None




		context = {
			'topic': topic,
			'object_id': object_id,
			'p': p,
			'object_slug': object_slug,
			'module_id': module_id,
		    'comments': comments,
		    'comment_form': comment_form,
		    'course': course,

		}
		return self.render_to_response(context)



	def post(self, request, *args, **kwargs):
		department = self.get_object()
		course = Department.objects.get(id=department.id, slug=department.slug)
		p = course
		#course = Department.objects.get(id=id, slug=slug)

		comment_form = CommentForm(request.POST or None)

		if 'topic_id' in self.kwargs:
		# get current module
			module = course.modules1.get(id=self.kwargs['topic_id'])
			comments = Comment.objects.filter(course=module, reply=None).order_by('-id')
			topic = department.modules1.get(id=self.kwargs['topic_id'])
			object_id = department.id
			object_slug = department.slug
			module_id = self.kwargs['topic_id']
		else:
		# get first module
			module = course.modules1.get(id=department.modules1.all()[0].id)
			comments = Comment.objects.filter(course=module, reply=None).order_by('-id')
			topic = department.modules1.all()[0]
			object_id = department.id
			object_slug = department.slug
			module_id = department.modules1.all()[0].id


		if comment_form.is_valid():
			content = request.POST.get('content')
			reply_id = request.POST.get('comment_id')
			comment_qs = None
			if reply_id:
			    comment_qs = Comment.objects.get(id=reply_id)
			comment = Comment.objects.create(course=module, user=request.user, content=content, reply=comment_qs)
			comment.save()
		comments1 = Comment.objects.filter(course=module, reply=None).order_by('-id')
		email_list = []
		if comments1:
		    for comment in comments1:
		        email = comment.user.email

		        if email in email_list:
		            pass
		        else:
		            email_list.append(email)

		email_list.append(settings.EMAIL_HOST_USER)

		if comment_form.is_valid():
		    content = request.POST.get('content')
		    reply_id = request.POST.get('comment_id')
		    email_msg = []
		    for email in email_list:
		        if str(email) == str(request.user.email):
		            pass
		        else:
		            email_msg.append(email)
		    if reply_id:
		        reply_email = []
		        comment_qs = Comment.objects.get(id=reply_id)
		        email_owner_comment = comment_qs.user.email
		        for reply in comment_qs.replies.all():
		            user_email = reply.user.email
		            if user_email in reply_email:
		                pass
		            else:
		                reply_email.append(user_email)
		            if email_owner_comment in reply_email:
		                pass
		            else:
		                reply_email.append(email_owner_comment)
		                print(reply_email)

		        reply_email_list = []
		        for mail in reply_email:
		            if str(mail) == str(request.user.email):
		                pass
		            else:
		                reply_email_list.append(mail)

		        reply_email_list.append(settings.EMAIL_HOST_USER)


		        subject = 'Comments reply from www.yctmarket.com'
		        message = '%s %s' %(comment_qs, f"\nreply by: {request.user.username} \n \nContent: \n{content} \n \n \nhttps://www.yctmarket.com{course.get_absolute_url()}",)

		        emailFrom = [settings.EMAIL_HOST_USER]
		        emailTo = reply_email_list
		        send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
		    else:
		        messge_content = f"Course: \n{course.name} \n \nComment by: {request.user} \n \nContent: \n{content} \n \n \nhttps://www.yctmarket.com{course.get_absolute_url()}"
		        subject = "New comment from forum"
		        message = '%s' %(messge_content)
		        emailFrom = [settings.EMAIL_HOST_USER]
		        emailTo = email_msg
		        send_mail(subject, message, emailFrom, emailTo, fail_silently=True )






		context = {
			'topic': topic,
			'object_id': object_id,
			'p': p,
			'object_slug': object_slug,
			'module_id': module_id,
		    'comments': comments,
		    'comment_form': comment_form,
		    'course': course,

		}


		if self.request.is_ajax():
			html = render_to_string('ent/comments.html', context, request=self.request)
			return JsonResponse({'form': html})








class StudentEnrollCourseView(LoginRequiredMixin, FormView):
	department = None
	form_class = CourseEnrollForm
	def form_valid(self, form):
		self.department = form.cleaned_data['department']
		self.department.students1.add(self.request.user)
		return super(StudentEnrollCourseView, self).form_valid(form)


	def get_success_url(self):
		return reverse_lazy('students1:student_department_detail', args=[self.department.id])




class StudentDepartmentListView(LoginRequiredMixin, ListView):
	model = Department
	# template_name = 'students/list.html'
	template_name = 'voting/list1.html'

	def get_queryset(self):
		qs = super(StudentDepartmentListView, self).get_queryset()
		return qs.filter(students__in=[self.request.user])


def _parse_body(body):
	body_unicode = body.decode('utf-8')
	return json.loads(body_unicode)

@csrf_exempt
def processPaystackWebhook2(request):
    if request.method == 'POST':
        json_body = json.loads(request.body)
        #paystack_sk = "sk_live_ffb5db8bf8d3abe7f343a743ae58ac5911c68d11"
        #paystack_sk = "sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111"
        print("print(json_body) here here")
        x_forwarded_for = request.META.get('HTTP_X_FORWADED_FOR')
        if x_forwarded_for:
        	ip = x_forwarded_for.split(',')[0]
        else:
        	ip = request.META.get('REMOTE_ADDR')
        paystac_ip = ["52.31.139.75", "52.49.173.169", "52.214.14.220", "10.0.0.124"]
        if str(ip) in paystac_ip:
            status = json_body['data']['status']
            if status == "success":
                reference = json_body['data']['reference']
                if reference:
        	        try:
        	            user_reference = PurchaseReference.objects.get(reference=reference)
        	            if user_reference:
        	                if user_reference.brand == "Department":
        	                    course = user_reference.course
        	                    user = user_reference.user
        	                    course.students.add(user)
        	                    subject = f"webhook from paystack via yctmarket"
        	                    message = '%s ' %(f"\nHello {user_reference.firstname} {user_reference.lastname} \n \nYour {user_reference.amount} NGN payment for {course.name} course has successfuly being verified and you have been added to the course.\n \nYou can now access the course contents by following the link below\n \n \nhttps://www.yctmarket.com{course.get_absolute_url()}",)
        	                    emailFrom = [settings.EMAIL_HOST_USER]
        	                    emailTo = [settings.EMAIL_HOST_USER, user_reference.email]
        	                    send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
        	                    return HttpResponse(status=200)
                	except ObjectDoesNotExist:
                		return HttpResponse(status=400)

    return HttpResponse(status=400)




def pay_for_course(request, id, slug):
	user = User.objects.get(username=request.user)
	firstname = user.first_name
	lastname = user.last_name
	email = user.email
	username = user.username
	brand = "Department"
	course = get_object_or_404(Department, id=id, slug=slug)
	if not course.amount:
		course.students.add(request.user)
		return redirect('students1:student_department_detail', pk=course.pk)
	elif course.instructor == user:
	    course.students.add(request.user)
	    return redirect('students1:student_department_detail', pk=course.pk)
	else:
	    course_name = course.name
	    course_slug = course.name
	    amount = int(str(course.amount) + "00")
	    r = PurchaseReference(firstname=firstname, lastname=lastname, email=email, amount=course.amount, brand=brand, course=course, user=user)
	    r.save()
	    reference = str(r.reference)

	    subject = f"Customer about to pay for {course_name} course at yctmarket"
	    message = '%s ' %(f"\nName: {firstname} {lastname} \n \nEmail: {email}\n \nUsername: {username}\n \nAmount: {course.amount} NGN\n \nReference: {reference}\n \nCourse: {course}",)
	    #message = '%s %s %s %s ' %(firstname, lastname, email, username)
	    emailFrom = [settings.EMAIL_HOST_USER]
	    emailTo = [settings.EMAIL_HOST_USER]
	    send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
	    headers = {
	        'Authorization': 'Bearer sk_live_ffb5db8bf8d3abe7f343a743ae58ac5911c68d11',
	        'Content-Type': 'application/json',
	        }
	    #sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111
	    #headers = {
	        #'Authorization': 'Bearer sk_test_3be5de37862bdd6a684d0f2fe08c2ef6dfbb5111',
	        #'Content-Type': 'application/json',
	        #}
	    data = {"reference": reference, "amount": amount, "email": email}
	    url = "https://api.paystack.co/transaction/initialize"
	    response = requests.request("POST", url, headers=headers, json=data)
	    res = response.json()

	    checkout = res['data']['authorization_url']
	    return redirect(checkout)


def assignment(request, id, slug, topic_id):
	#user = User.objects.get(username=request.user)
	course = Department.objects.get(id=id, slug=slug)
	module = course.modules1.get(id=topic_id)
	assignment = module.assignments1.all()


	ask = []
	if len(assignment) > 0:
	    for i in assignment:
	        if i.show_question == True:
	            pass
	        else:
	            ask.append(i)



	paginator = Paginator(ask, 1)
	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)

	score_questions = []
	score_answer = []
	if len(assignment) > 0:
		for assignmentt in assignment:
			question = assignmentt.question
			score = Score.objects.filter(user=request.user, module=module, question=question)
			for i in score:
			 	score_questions.append(i.question)
			 	score_answer.append(i.student_answer)
	else:
		score = None


	ask = []
	if len(assignment) > 0:
	    for i in assignment:
	        if i.show_question == True:
	            pass
	        else:
	            ask.append(i)


	loop_times = range(1, 17)
	context = {
        'assignment': assignment,
        'questions': questions,
        'id': id,
        'course': course,
        'slug': slug,
        'topic_id': topic_id,
        'score': score,
        'score_questions': score_questions,
        'score_answer': score_answer,
        'ask': ask,
        'loop_times': loop_times

    }
    # html = render_to_string('students1/assignment.html', context, request=request)
    # return JsonResponse({'form': html})

	return render(request, 'voting/assignment.html', context)




def vote_chart(request):
    if request.method == 'POST' and request.is_ajax():
        topic_id = request.POST['topic_id']
        course_id = request.POST['course_id']
        question_id = request.POST['question_id']
        course = Department.objects.get(id=course_id)
        module = Course.objects.get(id=topic_id)
        labels = []
        data = []
        print("hhere")


        #check is assignments exit in this module if true
        if len(module.assignments1.all()) > 0:
            t = module.assignments1.get(id=question_id)
            position = t.question

            if t.option1 != None:
                try:
                    option1 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option1).count()
                except:
                    option1 = None

                if option1 != None:
                    labels.append(t.option1)
                    data.append(int(option1))
                    print(option1)
                    print(t.option1)
                else:
                    labels.append(t.option1)
                    data.append(0)





            if t.option2 != None:
                try:
                    option2 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option2).count()
                except:
                    option2 = None

                if option1 != None:
                    labels.append(t.option2)
                    data.append(int(option2))
                else:
                    labels.append(t.option2)
                    data.append(0)





            if t.option3 != None:
                try:
                    option3 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option3).count()
                except:
                    option3 = None

                if option3 != None:
                    labels.append(t.option3)
                    data.append(int(option3))
                else:
                    labels.append(t.option3)
                    data.append(0)



            if t.option4 != None:
                try:
                    option4 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option4).count()
                except:
                    option4 = None

                if option4 != None:
                    labels.append(t.option4)
                    data.append(int(option4))
                else:
                    labels.append(t.option4)
                    data.append(0)


            if t.option5 != None:
                try:
                    option5 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option5).count()
                except:
                    option5 = None

                if option5 != None:
                    labels.append(t.option5)
                    data.append(int(option5))
                    print(option5)
                    print(t.option5)
                else:
                    labels.append(t.option5)
                    data.append(0)


            if t.option6 != None:
                try:
                    option6 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option6).count()
                except:
                    option6 = None

                if option6 != None:
                    labels.append(t.option6)
                    data.append(int(option6))
                    print(option6)
                    print(t.option6)
                else:
                    labels.append(t.option6)
                    data.append(0)


            if t.option7 != None:
                try:
                    option7 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option7).count()
                except:
                    option7 = None

                if option7 != None:
                    labels.append(t.option7)
                    data.append(int(option7))
                    print(option7)
                    print(t.option7)
                else:
                    labels.append(t.option7)
                    data.append(0)

            if t.option8 != None:
                try:
                    option8 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option8).count()
                except:
                    option8 = None

                if option8 != None:
                    labels.append(t.option8)
                    data.append(int(option8))
                    print(option8)
                    print(t.option8)
                else:
                    labels.append(t.option8)
                    data.append(0)

            if t.option9 != None:
                try:
                    option9 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option9).count()
                except:
                    option9 = None

                if option9 != None:
                    labels.append(t.option9)
                    data.append(int(option9))
                    print(option9)
                    print(t.option9)
                else:
                    labels.append(t.option9)
                    data.append(0)

            if t.option10 != None:
                try:
                    option10 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option10).count()
                except:
                    option10 = None

                if option10 != None:
                    labels.append(t.option10)
                    data.append(int(option10))
                    print(option10)
                    print(t.option10)
                else:
                    labels.append(t.option10)
                    data.append(0)


            if t.option11 != None:
                try:
                    option11 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option11).count()
                except:
                    option11 = None

                if option11 != None:
                    labels.append(t.option11)
                    data.append(int(option11))
                    print(option11)
                    print(t.option11)
                else:
                    labels.append(t.option11)
                    data.append(0)

            if t.option12 != None:
                try:
                    option12 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option12).count()
                except:
                    option12 = None

                if option12 != None:
                    labels.append(t.option12)
                    data.append(int(option12))
                    print(option12)
                    print(t.option12)
                else:
                    labels.append(t.option12)
                    data.append(0)

            if t.option13 != None:
                try:
                    option13 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option13).count()
                except:
                    option13 = None

                if option13 != None:
                    labels.append(t.option13)
                    data.append(int(option13))
                    print(option13)
                    print(t.option13)
                else:
                    labels.append(t.option13)
                    data.append(0)

            if t.option14 != None:
                try:
                    option14 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option14).count()
                except:
                    option14 = None

                if option14 != None:
                    labels.append(t.option14)
                    data.append(int(option14))
                    print(option14)
                    print(t.option14)
                else:
                    labels.append(t.option14)
                    data.append(0)

            if t.option15 != None:
                try:
                    option15 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option15).count()
                except:
                    option15 = None

                if option15 != None:
                    labels.append(t.option15)
                    data.append(int(option15))
                    print(option15)
                    print(t.option15)
                else:
                    labels.append(t.option15)
                    data.append(0)

            if t.option16 != None:
                try:
                    option16 = Score.objects.filter(course=course, module=module, question=position).filter(student_answer=t.option16).count()
                except:
                    option16 = None

                if option16 != None:
                    labels.append(t.option16)
                    data.append(int(option16))
                    print(option16)
                    print(t.option16)
                else:
                    labels.append(t.option16)
                    data.append(0)

        print(labels)
        print(data)
        context = {
            'labels': labels,
            'data': data,
            'position': position.upper(),
            'name1': course.name
        }

        #html = render_to_string('voting/chart.html', context, request=request)
        #return JsonResponse({'form': html})
        return JsonResponse(data={
        'labels': labels,
        'data': data,
        'position': position.upper(),
        'name1': course.name
    })










def saveans1(request, id, slug, topic_id, page_no):
	page_no1 = int(page_no) - 1

	user = User.objects.get(username=request.user)
	phone = PhoneNumber.objects.get(user=user)
	matric_number  = phone.matric_number
	department  = phone.department
	level = phone.level
	course = Department.objects.get(id=id, slug=slug)
	instructor = course.instructor
	instructor_email = instructor.email
	module = course.modules1.get(id=topic_id)
	modules = course.modules1.all()
	assignment = module.assignments1.all()[page_no1]
	question = assignment.question
	score_grade = Score.objects.filter(question=question)
	student_taken_assignment = []

	if request.is_ajax and request.method == 'POST':
		ans = request.POST['ans']
		student_answer = ans
		for i in score_grade:
			student_taken_assignment.append(i.user)
		if user in student_taken_assignment:
			pass
		else:
			if student_answer:
				grade = 1
				score = Score(user=user,
					course=course,
					module=module,
					assignment=assignment,
					question=question,
					student_answer=student_answer,
					score=grade)
				score.save()
				total = 0
			else:
				pass
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
        'department': department,
        'level': level,
        'course' : course,
        'module' : module,
        'modules' : modules,
        'assignment' : assignment,
        'scores' : scores,
        'id': id,
        'slug': slug,
    }

	html = render_to_string('voting/email_template.html', context, request=request)
	text_content = strip_tags(html)
	email = EmailMultiAlternatives(
		#subject

		f"{course.school} student grading {course.name} course",
		#content
		text_content,
		#from email
		settings.EMAIL_HOST_USER,
		#rec list
		[settings.EMAIL_HOST_USER, instructor_email]
		#[settings.EMAIL_HOST_USER]
		#[instructor_email]
		)
	email.attach_alternative(html, "text/html")
	email.send()
	# student_department_list
	return redirect('students1:student_department_detail', course.id)
	#return render(request, 'voting/email_template.html', context)



class StudentAssesmentDetailView(LoginRequiredMixin, DetailView):
	model = Course
	template_name = 'students1/assignment.html'

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
			context['topic'] = department.modules1.all()[0]
		return context



