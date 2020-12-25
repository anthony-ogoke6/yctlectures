from django.contrib import admin
from .models import Product, Shops, Stores
# Register your models here.


Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}



class StoresAdmin(admin.ModelAdmin):
    list_display = ['storename', 'owner', 'created']
    #list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'storename')
    prepopulated_fields = {'slug':('storename',)}
    #list_editable = ('status',)
    date_hierarchy = ('created')



class ShopsAdmin(admin.ModelAdmin):
    list_display = ['storename', 'owner', 'created']
    #list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'storename')
    prepopulated_fields = {'slug':('storename',)}
    #list_editable = ('status',)
    date_hierarchy = ('created')


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'amount', 'status', 'available', 'author', 'created', 'updated']
    #list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'updated')
    search_fields = ('author__username', 'title')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')




class InfiniteScrollAdmin(admin.ModelAdmin):
    list_display = ('start', 'end')


admin.site.register(Product, ProductAdmin)
admin.site.register(Shops, ShopsAdmin)
