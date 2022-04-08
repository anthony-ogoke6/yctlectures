from django.contrib import admin
from .models import Article, AdvertImages, Profile, Post, PurchaseReference, InfiniteScroll, Category, PhoneNumber, Comment, Images, Face, Departments
from shops.models import Stores


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}



class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']



class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'amount', 'stock', 'status', 'available', 'author', 'created', 'updated']
    #list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'amount', 'stock', 'status', 'available', 'author', 'created', 'updated']
    #list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')



class FaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug','status', 'author', 'created', 'updated']
    #list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')


class InfiniteScrollAdmin(admin.ModelAdmin):
    list_display = ('start', 'end')

class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ['user__username']


class StoresAdmin(admin.ModelAdmin):
    list_display = ('storename',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')


class PurchaseReferenceAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'reference', 'email')



#class ImagesAdmin(admin.ModelAdmin):
    #list_display = ('post', 'image')

class AdvertImagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'amount', 'duration')
    prepopulated_fields = {"slug":("title",)}
    #autocomplete_fields = ['department']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(PurchaseReference, PurchaseReferenceAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Stores, StoresAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Face, FaceAdmin)
admin.site.register(AdvertImages, AdvertImagesAdmin)
admin.site.register(InfiniteScroll, InfiniteScrollAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Comment)
admin.site.register(Images)

