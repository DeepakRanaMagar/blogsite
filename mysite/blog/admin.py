from django.contrib import admin
from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author','publish','status')
    list_filter = ('status', 'created','publish', 'author')
    search_fields=('title', 'body')
    raw_id_fields=('author',) #tuples 
    date_hierarchy='publish'
    ordering = ['status', 'publish']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)