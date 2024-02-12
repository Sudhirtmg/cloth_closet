from User_app import views
from django.urls import path,include

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('customer/', views.customer, name='customer'),
    path('company/', views.employee, name='employee'),
    path('signout/',views.singout,name='signout'),
    path('customer/<username>/', views.UserProfile, name='profile'),
    path('company/<username>/', views.CompanyUserProfile, name='companyprofile'),



    
]