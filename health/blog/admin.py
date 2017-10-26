from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
	list_display = ['author','created']
	list_filter = ['author','created']
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Blog,BlogAdmin)