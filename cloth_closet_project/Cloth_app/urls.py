from django.urls import path,include
from Cloth_app import views
urlpatterns = [
path('',views.index,name='home'),
path('newpost', views.NewPost, name='newpost'),
path('customer/<uuid:post_id>', views.PostDetail, name='post-details'),
path('company/<uuid:id>', views.companyPostDetail, name='companypost-details'),
path('company/serach-result/',views.search_view,name='search-result'),
     path('company/category/',views.category_list,name="category"),
 path('company/category_Post_list/<cid>/',views.category_Post_list,name="category-post-list"),

]