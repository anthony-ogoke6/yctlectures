from django.shortcuts import render

# Create your views here.
from django.apps import apps
from django.core.cache import cache
from django.db.models import Count
from django.forms.models import modelform_factory

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin

from .forms import ModuleFormSet, CreateForm, AssignmentForm, ModuleFormSet1, DepartmentForm
from .models import School, Department, Course, Content, Assignment
from ent.models import PhoneNumber
from students.forms import CourseEnrollForm


import xlwt

from django.contrib.auth.models import User


import datetime

import logging

logger = logging.getLogger(__name__)



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
    fields = ['school', 'department_access', 'name']
    success_url = reverse_lazy('voting:manage_department_list')
    template_name = 'voting/form.html'


class OwnerAssignmentEditMixin(AssignmentMixin, AssignmentEditMixin):
    fields = ['question', 'option1', 'option2', 'option3', 'option4', 'description', 'answer']
    success_url = reverse_lazy('voting:manage_department_list')
    template_name = 'voting/form.html'



class ManageDepartmentListView(PermissionRequiredMixin, OwnerDepartmentMixin, ListView):
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


class DepartmentCreateView(PermissionRequiredMixin, OwnerDepartmentEditMixin, CreateView):
	permission_required = 'voting.add_department'
	success_message = "Course was created succesfully."
	#form_class = CreateForm


class DepartmentUpdateView(PermissionRequiredMixin, OwnerDepartmentEditMixin, UpdateView):
    template_name = 'voting/form.html'
    permission_required = 'voting.change_department'
    # form_class = CreateForm

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

class DepartmentDeleteView(PermissionRequiredMixin, OwnerDepartmentMixin, DeleteView):
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
			formset.save()

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
				messages.success(request, "Chapter has been edited successfully.", extra_tags='success')
				return redirect('voting:topic_content_list', self.topic.id)
			return self.render_to_response({'form': form, 'object': self.obj})




class ContentDeleteView(View):
	def post(self, request, id):
		content = get_object_or_404(Content, id=id, topic__course__instructor=request.user)
		topic = content.topic
		content.item.delete()
		content.delete()
		return redirect('voting:topic_content_list', topic.id)



class CourseContentListView(TemplateResponseMixin, View):
	template_name = 'voting/content_list.html'
	def get(self, request, topic_id):
		topic = get_object_or_404(Course, id=topic_id, course__instructor=request.user)

		assignment = topic.assignments.filter(course__course__instructor=request.user)
		return self.render_to_response({'topic': topic, 'assignment': assignment})




class CourseOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

	def post(self, request):
		for id, order in self.request_json.items():
			cos = Course.objects.filter(id=id, course__instructor=request.user)
			for u in cos:
				Course.objects.filter(id=id, course__instructor=request.user).update(order=order)
				course = Course.objects.filter(id=id, course__instructor=request.user)


		return self.render_json_response({'saved': 'OK'})


# class CourseOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
#  	def post(self, request):
#  		logger.error("Test!!")
#  		for id, order in self.request_json.items():
#  			course = Course.objects.filter(id=id, course__instructor=request.user)
#  			course.order = order
#  			course.save()
#  		return self.render_json_response({'saved': 'OK'})





class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Content.objects.filter(id=id, topic__course__instructor=request.user).update(order=order)
		return self.render_json_response({'saved': 'OK'})



class DepartmentListView(TemplateResponseMixin, View):
	model = Department
	template_name = 'voting/course/list.html'

	def get(self, request):
		name = request.GET.get('name')
		departments = self.model.objects.all()
		if name:
			departments = departments.filter(name__icontains=name)
		return self.render_to_response({'departments': departments})
		# schools = cache.get('all_schools')
		# if not schools:
		# 	schools = School.objects.annotate(total_courses=Count('courses'))
		# 	cache.set('all_schools', schools)

		# all_departments = Department.objects.annotate(total_modules=Count('modules'))
		# #departments = Department.objects.annotate(total_modules=Count('modules'))
		# if school:
		# 	school = get_object_or_404(School, slug=school)
		# 	key = 'school_{}_departments'.format(school.id)
		# 	departments = cache.get(key)
		# 	if not departments:
		# 		departments = all_departments.filter(school=school)
		# 		cache.set(key, departments)
		# else:
		# 	departments = cache.get('all_departments')
		# 	if not departments:
		# 		departments = all_departments
		# 		cache.set('all_departments', departments)
		# 		#departments = departments.filter(school=school)
		#return self.render_to_response({'schools': schools, 'school': school, 'departments': departments})



class DepartmentDetailView(DetailView):
	model = Department
	template_name = 'voting/course/detail.html'


	def get_context_data(self, **kwargs):
		context = super(DepartmentDetailView, self).get_context_data(**kwargs)
		context['enroll_form'] = CourseEnrollForm(initial={'department':self.object})
		phone = PhoneNumber.objects.get(user=self.object.instructor)
		context['phone'] = phone.prefix
		qs = super(DepartmentDetailView, self).get_queryset()
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
				for obj in formset.deleted_objects:
					obj.delete()
				assignment.course = course
				assignment.save()
			# post.course = course

			# subject = f"An instructor just uploaded assignment question in to their course."
			# message = '%s %s %s ' %(title, amount, user)
			# emailFrom = [settings.EMAIL_HOST_USER]
			# emailTo = [settings.EMAIL_HOST_USER]
			# send_mail(subject, message, emailFrom, emailTo, fail_silently=True )
			messages.success(request, "Assignment has been successfully added.")
			return redirect('voting:topic_content_list', topic_id=topic_id)
	else:
		formset = ModuleFormSet1()
	context = {
		'formset': formset,
	}
	return render(request, 'voting/content/form1.html', context)



def edit_assignment(request, topic_id, slug, course_id):
	course = Course.objects.get(id=topic_id)
	if request.method == 'POST':
		formset = ModuleFormSet1(instance=course, data=request.POST)
		if formset.is_valid():
			for form in formset.forms:
				assignment = form.save(commit=False)
				for obj in form.deleted_objects:
					obj.delete()
				assignment.course = course
				assignment.save()
				messages.success(request, "Assignment has been successfully edited.")
			return redirect('voting:topic_content_list', topic_id=topic_id)
	else:
		formset = ModuleFormSet1(instance=course)
	context = {
		'formset': formset,
	}
	return render(request, 'voting/content/form1.html', context)


def students(request, course_id, slug):
	course = Department.objects.get(id=course_id)
	students = course.students.all()
	about = PhoneNumber.objects.all()
	departments = School.objects.all()
	course_department = course.department_access_course
	for i in departments:
		if i in list(course_department):
			print(i)
	department_access = []
	form = DepartmentForm(instance=course)
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
		'course_department': course_department
	}
	return render(request, 'voting/students.html', context)



def delete_student(request, course_id, slug, student):
	course = Department.objects.get(id=course_id)
	students = course.students.all()
	student = User.objects.get(username=student)
	if student in students:
		course.students.remove(student)
	return redirect('voting:students', course_id=course_id, slug=slug)




def export_users_xls(request, course_id, slug):
	course = Department.objects.get(id=course_id)
	modules = course.modules.all()
	students = course.students.all()
	about_students = PhoneNumber.objects.all()

	all_departments = course.department_access
	department = request.POST['department']


	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = f'attachment; filename={course.name}' + f'_{department}_' + str(datetime.datetime.now()) + '.xls"'

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

	for student in students:
		for i in about_students:
			if student.username == i.user.username:
				if i.department == department:
					full_name = str(student.last_name) + " " + str(student.first_name)
					rows.append(full_name)
					if i.matric_number:
						matric_number = i.matric_number
					else:
						matric_number = int(0)
					row.append(matric_number)
					grade = []
					#take all modules and iterate
					for j in modules:
						#check is assignments exit in this module if true
						if len(j.assignments.all()) > 0:
							assignments = j.assignments.all()
							for t in assignments:
								question = t.question
								try:
									scoring = Score.objects.get(user=user, course=course, question=question)
									score = scoring.score
									grade.append(int(score))
								except:
									grade.append(int(0))
							total_question = sum(grade)
							row.append(total_question)
						else:
							row.append(int(0))


					sum_total = sum(row[2:])
					row.append(sum_total)






	#rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')

	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response
