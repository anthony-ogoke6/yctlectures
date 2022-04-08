from django.shortcuts import render

# Create your views here.
from django.apps import apps
from django.core.cache import cache
from django.db.models import Count, Q
from django.forms.models import modelform_factory

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

import xlwt

from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required



from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from braces.views import LoginRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin

from .forms import ModuleFormSet, CreateForm, ModuleFormSet1, ModuleFormSet2, DepartmentForm
from .models import School, Department, Course, Content, Assignment, Score, Comment, DepartmentalAccess, DepartmentalAccessLevel
from ent.models import PhoneNumber
from students.forms import CourseEnrollForm

from django.template.loader import render_to_string

import django_excel as excel

import datetime
from django.core import serializers
from django.forms.models import model_to_dict


import logging
import json

logger = logging.getLogger(__name__)


#class UploadFileForm(forms.Form):
    #file = forms.FileField()



# Create your views here.
class AssignmentMixin(object):
    def get_queryset(self):
    	course = Department.objects.get(id=self.kwargs['course_id'], slug=self.kwargs['slug'])
    	qs = super(AssignmentMixin, self).get_queryset()

    	return qs.filter(course=course)




class AssignmentEditMixin(object):
	def form_valid(self, form):
		course = Department.objects.get(id=self.kwargs['course_id'], slug=self.kwargs['slug'])
		form.instance.course = course
		return super(AssignmentEditMixin, self).form_valid(form)




class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(instructor=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerDepartmentMixin(OwnerMixin, LoginRequiredMixin):
    model = Department
    fields = ['school', 'name', 'amount','overview', 'photo']
    success_url = reverse_lazy('voting:manage_department_list')




class OwnerAssignmentMixin(AssignmentMixin, AssignmentEditMixin):
	model = Assignment
	fields = ['question', 'option1', 'option2', 'option3', 'option4', 'description', 'answer']
	success_url = reverse_lazy('voting:manage_department_list')
	template_name = 'voting/form.html'




class OwnerDepartmentEditMixin(OwnerDepartmentMixin, OwnerEditMixin):
    fields = ['school', 'department_access', 'level', 'name', 'amount', 'overview', 'photo']
    success_url = reverse_lazy('voting:manage_department_list')
    template_name = 'voting/form.html'


class OwnerAssignmentEditMixin(AssignmentMixin, AssignmentEditMixin):
    fields = ['question', 'option1', 'option2', 'option3', 'option4', 'description', 'answer']
    success_url = reverse_lazy('voting:manage_department_list')
    template_name = 'voting/form.html'



class ManageDepartmentListView(OwnerDepartmentMixin, ListView):
    model = Department
    template_name = 'voting/list.html'
    permission_required = 'voting.view_department'
    raise_exception = True
    permission_denied_message = "Permission Denied"
    paginate_by = 6
    context_object_name = 'articles'
    def get_queryset(self):
    	qs = super(ManageDepartmentListView, self).get_queryset()
    	return qs.filter(instructor=self.request.user)


class DepartmentCreateView(OwnerDepartmentEditMixin, CreateView):
	permission_required = 'voting.add_department'
	#form_class = CreateForm

	def form_valid(self, form):
	    allow2 = []
	    allow = []
	    obj = form.save(commit=False)
	    school = form.cleaned_data['school']
	    #school = School.objects.get(name=school)
	    allow_form = self.request.POST.getlist('department_access')
	    allow_form2 = self.request.POST.getlist('level')
	    #allow.append(school.name)
	    for h in allow_form2:
	        if h != '':
	            if h not in allow2:
	                allow2.append(h)

	    for i in allow_form:
	        if i != '':
	            if i not in allow:
	                allow.append(i)
	    obj.department_access_course = allow
	    obj.instructor = self.request.user
	    obj.save()
	    course = Department.objects.get(school=school, instructor=self.request.user, name=self.request.POST['name'])
	    print(course)
	    for g in allow2:
	        new_level_access = DepartmentalAccessLevel(name=g, course=course)
	        new_level_access.save()

	    for i in allow:
	        new_department_access = DepartmentalAccess(name=i, course=course)
	        new_department_access.save()
	    return redirect('voting:manage_department_list')

class DepartmentUpdateView(OwnerDepartmentEditMixin, UpdateView):
    template_name = 'voting/form.html'
    permission_required = 'voting.change_department'

    def form_valid(self, form):
        allow = []
        allow2 = []
        obj = form.save(commit=False)
        school = form.cleaned_data['school']
        name = self.request.POST['name']
        #allow.append(obj.school.name)
        allow_form = self.request.POST.getlist('department_access')
        allow_form2 = self.request.POST.getlist('level')

        for h in allow_form2:
	        if h != '':
	            if h not in allow2:
	                allow2.append(h)


        for i in allow_form:
            if i != '':
                if i not in allow:
                    allow.append(i)
        obj.department_access_course = allow
        obj.instructor = self.request.user
        obj.save()
        course = Department.objects.get(school=school, instructor=self.request.user, name=name)
        print(course)

        for g in allow2:
            new_level_access = DepartmentalAccessLevel(name=g, course=course)
            new_level_access.save()


        for i in allow:
	        new_department_access = DepartmentalAccess(name=i, course=course)
	        new_department_access.save()


        return redirect('voting:manage_department_list')


    def get_context_data(self, **kwargs):
        context = super(DepartmentUpdateView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            d =[]
            b = []
            a = DepartmentalAccess.objects.filter(course=self.object)

            f = DepartmentalAccessLevel.objects.filter(course=self.object)

            for c in f:
                if c.name not in d:
                    d.append(c.name)
                    context['level'] = d

            for i in a:
                if i.name not in b:
                    b.append(i.name)
                    context['department_access'] = b
            context['a'] = b
            context['d'] = d
        #qs = super(DepartmentUpdateView, self).get_queryset()
        return context

    # def post(self, request):
    # 	post_data = request.POST or None
    # 	file_data = request.FILES or None

    # 	form = CreateForm(post_data, file_data, instance=)
    # 	if form.is_valid():
    # 		form.save()
    # 		message.success(request, "Your course was succesfully updated!")
    # 		return HttpResponseRedirect(reverse_lazy('profile'))

    # 	context = self.get_context_data(
    # 									form=form
    # 									)
    # 	return self.render_to_response(context)

    # def get(self, request, *args, **kwargs):
    # 	return self.post(request, *args, **kwargs)

class DepartmentDeleteView(OwnerDepartmentMixin, DeleteView):
	pk_url_kwarg = 'pk'
	template_name = 'voting/delete.html'
	success_url = reverse_lazy('voting:manage_department_list')
	permission_required = 'voting.delete_department'



class DepartmentCourseUpdateView(TemplateResponseMixin, View):
	template_name = 'voting/formset.html'
	course = None
	def get_formset(self, data=None):
		return ModuleFormSet(instance=self.course, data=data)

	def dispatch(self, request, pk):
		self.course = get_object_or_404(Department, id=pk, instructor=request.user)
		return super(DepartmentCourseUpdateView, self).dispatch(request, pk)

	def get(self, request, *args, **kwargs):
		formset = self.get_formset()
		return self.render_to_response({'course': self.course, 'formset': formset})

	def post(self, request, *args, **kwargs):
		formset = self.get_formset(data=request.POST)
		if formset.is_valid():
		    for form in formset:
		        course_update = form.save(commit=False)
		        course_update.course = self.course
		        course_update.save()
		    messages.success(request, "Chapter has been updated successfully.", extra_tags='success')
		    return redirect('voting:manage_department_list')
		return self.render_to_response({'course': self.course, 'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
	topic = None
	model = None
	obj = None
	template_name = 'voting/content/form.html'

	def get_model(self, model_name):
		if model_name in ['text', 'video', 'image', 'file']:
			#self.fields['goal_status'].queryset = self.fields['goal_status'].queryset.exclude(status_name=status_name).exclude(status_name=sname)
			return apps.get_model(app_label='voting', model_name=model_name)
		return None

	def get_form(self, model, *args, **kwargs):
		Form = modelform_factory(model, exclude=['instructor', 'owner', 'order', 'created', 'updated'])
		return Form(*args, **kwargs)

	def dispatch(self, request, topic_id, model_name, id=None):
		self.topic = get_object_or_404(Course, id=topic_id, course__instructor=request.user)
		self.model = self.get_model(model_name)
		if id:
			self.obj = get_object_or_404(self.model, id=id, owner=request.user)
		return super(ContentCreateUpdateView, self).dispatch(request, topic_id, model_name, id)


	def get(self, request, topic_id, model_name, id=None):
		form = self.get_form(self.model, instance=self.obj)
		return self.render_to_response({'form': form, 'object': self.obj})

	def post(self, request, topic_id, model_name, id=None):
		form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

		if form.is_valid():
			obj = form.save(commit=False)
			obj.instructor = request.user
			obj.owner = request.user
			obj.save()
			if not id:
				# new content
				Content.objects.create(topic=self.topic, item=obj)
				messages.success(request, "Content has been edited successfully.", extra_tags='success')
				return redirect('voting:topic_content_list', self.topic.id)
			return self.render_to_response({'form': form, 'object': self.obj})




class ContentDeleteView(View):
	def post(self, request, id):
		content = get_object_or_404(Content, id=id, topic__course__instructor=request.user)
		topic = content.topic
		content.item.delete()
		content.delete()
		messages.success(request, "Content has been deleted successfully.", extra_tags='error')
		return redirect('voting:topic_content_list', topic.id)



class CourseContentListView(TemplateResponseMixin, View):
	template_name = 'voting/content_list.html'
	def get(self, request, topic_id):
		print('check check')
		topic = get_object_or_404(Course, id=topic_id, course__instructor=request.user)

		assignment = topic.assignments1.filter(course__course__instructor=request.user)
		return self.render_to_response({'topic': topic, 'assignment': assignment})




class CourseOrderView1(CsrfExemptMixin, JsonRequestResponseMixin, View):

	def post(self, request):
		for id, order in self.request_json.items():
			cos = Course.objects.filter(id=id, course__instructor=request.user)
			for u in cos:
				Course.objects.filter(id=id, course__instructor=request.user).update(order=order)
				#course = Course.objects.filter(id=id, course__instructor=request.user)



		return self.render_json_response({'saved': 'OK'})


class CourseOrderView2(CsrfExemptMixin, JsonRequestResponseMixin, View):

	def post(self, request):
		for id, order in self.request_json.items():
			cos = Course.objects.filter(id=id, course__instructor=request.user)
			for u in cos:
				print(u)
				Course.objects.filter(id=id, course__instructor=request.user).update(order=order)
				course = Course.objects.filter(id=id, course__instructor=request.user)


		return self.render_json_response({'saved': 'OK'})



class CourseOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Course.objects.filter(id=id, course__owner=request.user).update(order=order)
		return self.render_json_response({'saved': 'OK'})





class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Content.objects.filter(id=id, topic__course__instructor=request.user).update(order=order)
		return self.render_json_response({'saved': 'OK'})



class DepartmentListView(TemplateResponseMixin, View):
	model = Department
	template_name = 'voting/course/list.html'

	def get(self, request):
		name = request.GET.get('q')
		departments = self.model.objects.all()
		if name:
		    departments = departments.filter(
		        Q(name__icontains=name)|
		        Q(overview__icontains=name)|
		        Q(instructor__first_name__icontains=name)|
		        Q(instructor__last_name__icontains=name)|
		        Q(instructor__username__icontains=name)|
		        Q(school__name__icontains=name))
		paginator = Paginator(departments, 4)
		page = request.GET.get('page')
		try:
		    departments = paginator.page(page)
		except PageNotAnInteger:
		    departments = paginator.page(1)
		except EmptyPage:
		    departments = paginator.page(paginator.num_pages)
		return self.render_to_response({'departments': departments, 'name': name})



class DepartmentDetailView(DetailView):
	model = Department
	template_name = 'voting/course/detail.html'


	def get_context_data(self, **kwargs):
		context = super(DepartmentDetailView, self).get_context_data(**kwargs)
		context['enroll_form'] = CourseEnrollForm(initial={'department':self.object})
		phone = PhoneNumber.objects.get(user=self.object.instructor)
		context['phone'] = phone.prefix
		print(self.request.user.is_authenticated)
		#context['student'] = PhoneNumber.objects.get(user=self.request.user)
		if self.request.user.is_authenticated:
		    context['student'] = PhoneNumber.objects.get(user=self.request.user)
		    b = []
		    a = DepartmentalAccess.objects.filter(course=self.object)
		    #b.append(self.object.school.name)
		    if a:
		        for i in a:
		            if i.name not in b:
		                b.append(i.name)
		    context['department_access'] = b

		    c = []
		    d = DepartmentalAccessLevel.objects.filter(course=self.object)
		    if d:
		        for i in d:
		            if i.name not in c:
		                c.append(i.name)
		    context['department_access_level'] = c
		qs = super(DepartmentDetailView, self).get_queryset()
		# print('self.request.user')
		# print(self.request.user)
		# if self.request.user != 'AnonymousUser':
		# 	courses_students_is_in = qs.filter(students__in=[self.request.user])
		# 	context['courses_students_is_in'] = courses_students_is_in
		# else:
		# 	pass
		return context




#@login_required(login_url="user_login")
def add_assignment(request, topic_id, slug, course_id):
	course = Course.objects.get(id=topic_id)
	if request.method == 'POST':
		formset = ModuleFormSet1(request.POST)
		if formset.is_valid():
			for form in formset.forms:
				assignment = form.save(commit=False)
				assignment.course = course
				assignment.save()
			# post.course = course

			# subject = f"An instructor just uploaded assignment question in to their course."
			# message = '%s %s %s ' %(title, amount, user)
			# emailFrom = [settings.EMAIL_HOST_USER]
			# emailTo = [settings.EMAIL_HOST_USER]
			# send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
			messages.success(request, "Assignment has been added successfully.", extra_tags='success')
			return redirect('voting:topic_content_list', topic_id=topic_id)
	else:
		formset = ModuleFormSet1()
	context = {
		'formset': formset,
	}
	return render(request, 'voting/content/form3.html', context)



def edit_assignment(request, topic_id, slug, course_id):
	course = Course.objects.get(id=topic_id)
	if request.method == 'POST':
		formset = ModuleFormSet1(instance=course, data=request.POST)
		if formset.is_valid():
			for form in formset.forms:
				assignment = form.save(commit=False)
				assignment.course = course
				for i in formset.deleted_forms:
				    print(i)
				    print("formset forms")
				    print(formset.deleted_forms)
				    print(i)
				assignment.save()
				messages.success(request, "Assignment has been edited successfully.", extra_tags='success')
			return redirect('voting:topic_content_list', topic_id=topic_id)
	else:
		formset = ModuleFormSet1(instance=course)
	context = {
		'formset': formset,
	}
	return render(request, 'voting/content/form1.html', context)




@permission_required('voting.add_department')
def students(request, course_id, slug):
	course = Department.objects.get(id=course_id)
	students = course.students.all()
	about = PhoneNumber.objects.all()
	departmental_access = DepartmentalAccess.objects.filter(course=course)
	department_access = []
	form = DepartmentForm()
	course_department= course.department_access_course
	course_dept = course.school
	department_access.append(course_dept.name)
	for d in departmental_access:
	    print(d.name)
	    if d.name in department_access:
	        pass
	    else:
	        department_access.append(d.name)
	print(department_access)
	for student in students:
		for i in about:
			if student.username == i.user.username:
				print(i.matric_number)
	#print(course)

	context = {
		'students': students,
		'about': about,
		'course': course,
		'form': form,
		'course_department': course_department,
		'department_access': department_access
	}
	return render(request, 'voting/students.html', context)



def delete_student(request):
    if request.is_ajax and request.method == 'POST':
        course_id = request.POST['course_id']
        course_slug = request.POST['course_slug']
        username = request.POST['username']
        about = PhoneNumber.objects.all()

        print(username)
        print(course_id)
        print(course_slug)

        course = Department.objects.get(id=course_id, slug=course_slug)
        print(course)
        stud = course.students.all()
        print(stud)
        student = User.objects.get(username=username)
        if student in stud:
            course.students.remove(student)
        students = course.students.all()
        print(students)

    context = {
		'course_id': course_id,
		'course_slug': course_slug,
		'course_slug': course_slug,
		'students': students,
		'course': course,
		'about': about
	}
    if request.is_ajax():
        html = render_to_string('voting/stud.html', context, request=request)
        return JsonResponse({'form': html})




def export_users_xls(request, course_id, slug):
	course = Department.objects.get(id=course_id)
	modules = course.modules.all()
	students = course.students.all()
	about_students = PhoneNumber.objects.all()
	#form = DepartmentForm(request.POST)

	#all_departments = course.department_access
	department = request.POST.get('department', None)
	course_name = (str(course.name)).upper()

	date = datetime.datetime.now()
	#now = date.strftime('%d, %b %Y')



	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = f'attachment; filename={department}' + f'__{course_name}__' + str(date) + '.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')

	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ["Name", "Matric No."]
	for i in modules:
		if len(i.assignments.all()) > 0:
			columns.append(str(i.name) + "_Score")
	columns.append("Total")

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)


	font_style = xlwt.XFStyle()

	rows = []
	rows1 = []

	for student in students:
		for i in about_students:
			if student.username == i.user.username:
				if i.department == department:
					full_name = (str(student.last_name)).upper() + " " + (str(student.first_name)).upper()
					rows1.append(full_name)
					if i.matric_number:
						matric_number = str(i.matric_number).upper()
					else:
						matric_number = int(0)
					rows1.append(matric_number)
					grade = []
					#take all modules and iterate
					for j in modules:
						#check is assignments exit in this module if true
						if len(j.assignments.all()) > 0:
							assignments = j.assignments.all()
							for t in assignments:
								question = t.question
								try:
									scoring = Score.objects.get(user=i.user, course=course, question=question)
									score = scoring.score
									grade.append(int(score))

								except:
									grade.append(0)
							total_question = sum(grade)
							rows1.append(total_question)
							grade = []



					sum_total = sum(rows1[2:])
					#print(rows[2:6])
					rows1.append(sum_total)
					print(tuple(rows1))
					rows.append(tuple(rows1))
					rows1 = []
					#rows.append(sum_total)






	#rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')

	print(rows[:6])
	data = sorted(rows, key=lambda x: x[1])
	print(data)
	for row in data:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response


def delete_department_access(request):
    if request.is_ajax and request.method == 'POST':
        name_of_dept_for_deletion_ajax = request.POST['ans']
        name_of_course_from_ajax = request.POST['course']
        name_of_dept_from_ajax = request.POST['school']
        obj_name_of_department_for_this_course = School.objects.get(name=name_of_dept_from_ajax)
        department = Department.objects.get(school=obj_name_of_department_for_this_course, name=name_of_course_from_ajax)
        levels = ['ND1', 'ND2', 'ND3', 'HND1', 'HND2', 'HND3', '100L', '200L', '300L', '400L']
        if name_of_dept_for_deletion_ajax in levels:
            name_of_departmental_access = DepartmentalAccessLevel.objects.filter(name=name_of_dept_for_deletion_ajax, course=department)

            for i in name_of_departmental_access:
                i.delete()

            level = []
            a = DepartmentalAccessLevel.objects.filter(course=department)
            #dept.append(obj_name_of_department_for_this_course.name)
            for i in a:
                if i.name not in level:
                    level.append(i.name)

            dept = []
            b = DepartmentalAccess.objects.filter(course=department)
            dept.append(obj_name_of_department_for_this_course.name)
            for k in b:
                if k.name not in dept:
                    dept.append(k.name)

        else:
            name_of_departmental_access = DepartmentalAccess.objects.filter(name=name_of_dept_for_deletion_ajax, course=department)
            for i in name_of_departmental_access:
                i.delete()

            dept = []
            b = DepartmentalAccess.objects.filter(course=department)
            dept.append(obj_name_of_department_for_this_course.name)
            for k in b:
                if k.name not in dept:
                    dept.append(k.name)

            level = []
            a = DepartmentalAccessLevel.objects.filter(course=department)
            for i in a:
                if i.name not in level:
                    level.append(i.name)


    context = {
		'dept': dept,
		'level': level
	}
    if request.is_ajax():
        html = render_to_string('ent/dept.html', context, request=request)
        return JsonResponse({'form': html})





