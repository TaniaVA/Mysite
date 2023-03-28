from django.contrib import admin

from .models import Blog, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class BlogAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

# Register your models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)