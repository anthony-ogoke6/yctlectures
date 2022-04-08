from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from . import views
from learn import views as students_view

app_name = 'students'

urlpatterns = [

	path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
	re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<topic_id>\d+)/(?P<page_no>[\w-]+)/saveans/', views.saveans1, name='saveans1'),
	re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<topic_id>\d+)/assignment/$', views.assignment, name='assignment_module'),
	path('<course_id>/<slug>/students/', students_view.students, name='students'),
	path('course/<course_id>/<slug>/excel/', students_view.export_users_xls, name='export_users_xls'),
	path('delete/student/', students_view.delete_student, name='delete_student'),
	path('enroll-course/', views.StudentEnrollCourseView.as_view(), name='student_enroll_department'),
	path('dept/', views.StudentDepartmentListView.as_view(), name='student_department_list'),
	path('dept/<pk>/', views.StudentDepartmentDetailView.as_view(), name='student_department_detail'),
	re_path(r'(?P<id>\d+)/(?P<slug>[\w-]+)/pay_for_course/$', views.pay_for_course, name="pay_for_course"),
	path('dept/<pk>/<topic_id>/', views.StudentDepartmentDetailView.as_view(), name='student_department_detail_module'),
]

