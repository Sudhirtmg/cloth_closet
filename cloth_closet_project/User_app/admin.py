from django.contrib import admin
from User_app.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=['username','is_user','is_company']
admin.site.register(User,UserAdmin)