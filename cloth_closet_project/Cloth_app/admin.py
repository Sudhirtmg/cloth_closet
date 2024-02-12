from django.contrib import admin
from Cloth_app.models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','category_image']

class PostAdmin(admin.ModelAdmin):
    list_display=['caption','picture','posted','status','category']

admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)

