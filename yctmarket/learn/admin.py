from django.contrib import admin
#admin.site.index_template = 'memcache_status/admin_index.html'
from .models import School, Department, Course, Assignment, Score, Comment, DepartmentalAccess, DepartmentalAccessLevel

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class CourseInline(admin.StackedInline):
    model = Course

class AssignmentInline(admin.StackedInline):
    model = Assignment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'created']
    list_filter = ['created', 'school']
    search_fields = ['name', 'overview']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CourseInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course']
    search_fields = ['name', 'description']
    inlines = [AssignmentInline]
    # Register your models here.



class DepartmentalAccessAdmin(admin.ModelAdmin):
    list_display = ['name', 'course']


class DepartmentalAccessLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'course']



class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']

admin.site.register(Score, ScoreAdmin)
admin.site.register(Comment)
admin.site.register(DepartmentalAccess, DepartmentalAccessAdmin)
admin.site.register(DepartmentalAccessLevel, DepartmentalAccessLevelAdmin)



