from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author','publish','status')
    list_filter = ('status', 'created','publish', 'author')
    search_fields=('title', 'body')
    raw_id_fields=('author',) #tuples 
    date_hierarchy='publish'
    ordering = ['status', 'publish']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Post, PostAdmin)