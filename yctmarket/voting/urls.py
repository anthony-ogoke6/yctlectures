from django.urls import path, re_path
from . import views


app_name = 'voting'

urlpatterns = [
	path('', views.DepartmentListView.as_view(), name='department_list'),
    path('mine/', views.ManageDepartmentListView.as_view(), name='manage_department_list'),
    #path('error_page/', views.error_page, name='error_page'),
    path('create/', views.DepartmentCreateView.as_view(),name='department_create'),
	path('school/<school>/', views.DepartmentListView.as_view(), name='department_list_school'),

	path('<slug>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    #path('topic/<topic_id>/<slug>/<course_id>', views.AssignmentCreateView.as_view(), name='add_assignment'),
    path('topic/<topic_id>/<slug>/<course_id>', views.add_assignment, name='add_assignment'),

    path('edit/topic/<topic_id>/<slug>/<course_id>', views.edit_assignment, name='edit_assignment'),

    #re_path(r'(?P<pk>\d+)/delete/$', views.department_delete, name="department_delete"),
    path('del/delete/deparmental_access',  views.delete_department_access, name='departmental_access_delete'),
    path('<int:pk>/delete/',  views.DepartmentDeleteView.as_view(), name='department_delete'),
    path('<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('<int:pk>/course/', views.DepartmentCourseUpdateView.as_view(), name='department_course_update'),
    path('topic/<topic_id>/', views.CourseContentListView.as_view(), name='topic_content_list'),
    path('topic/<topic_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='topic_content_create'),
	path('topic/<topic_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='topic_content_update'),
	path('content/<id>/delete/', views.ContentDeleteView.as_view(), name='topic_content_delete'),

	path('content/order/', views.ContentOrderView.as_view(), name='content_order'),


	#path('content/(?P<id>\d+)/delete/$', views.ContentDeleteView.as_view(), name='module_content_delete'),
    #re_path(r'(?P<pk>\d+)/delete/$', views.DepartmentDeleteView.as_view(), name='department_delete'),
]