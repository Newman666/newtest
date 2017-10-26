from django.contrib import admin
from .models import Profile, UserType, Gender, HealthProfile, MessageBox, Message, Application, Notice

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'user_type']

admin.site.register(Profile, ProfileAdmin)

class UserTypeAdmin(admin.ModelAdmin):
	list_display = ['user_type']
	prepopulated_fields = {'slug': ('user_type',)}

admin.site.register(UserType,UserTypeAdmin)

class GenderAdmin(admin.ModelAdmin):
	list_display= ['user_gender']
	prepopulated_fields = {'slug': ('user_gender',)}

admin.site.register(Gender,GenderAdmin)

class HealthProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(HealthProfile,HealthProfileAdmin)

class MessageBoxAdmin(admin.ModelAdmin):
	list_display = ['author','tosomeone']

admin.site.register(MessageBox,MessageBoxAdmin)

admin.site.register(Message)
admin.site.register(Application)
admin.site.register(Notice)