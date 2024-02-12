from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from User_app.views import *
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('User_app.urls')),
    path('', include('Cloth_app.urls')),
    path('message/', include('direct_app.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
