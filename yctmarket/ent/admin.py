from django.contrib import admin
from .models import Article, AdvertImages, Profile, Post, PurchaseReference, InfiniteScroll, Stores, Category # Images,  AdvertImages
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


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

class InfiniteScrollAdmin(admin.ModelAdmin):
    list_display = ('start', 'end')


class StoresAdmin(admin.ModelAdmin):
    list_display = ('storename',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')


class PurchaseReferenceAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'reference', 'email')



#class ImagesAdmin(admin.ModelAdmin):
    #list_display = ('post', 'image')

class AdvertImagesAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'amount', 'duration')

admin.site.register(Category, CategoryAdmin)
admin.site.register(PurchaseReference, PurchaseReferenceAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Stores, StoresAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(AdvertImages)
admin.site.register(InfiniteScroll, InfiniteScrollAdmin)

