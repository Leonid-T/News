from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    exclude = ['views_count', 'like']


admin.site.register(Post, PostAdmin)
