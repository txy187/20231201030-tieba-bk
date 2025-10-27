from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),  # 首页路由：/ → index.html
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # 详情页路由：/post/<int:id>/ → post_detail
    path('create/', views.post_create, name='create_post'),  # 发布页路由：/create/ → create_post
    path('search/', views.search_posts, name='search'),  # 搜索页路由：/search/ → search.html
    # 保留原有路由用于内部重定向
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
]