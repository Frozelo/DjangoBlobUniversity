from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('update-view-time/', views.update_time_view, name='update_view_time'),
    path('filter_posts_by_tags/', views.filter_posts_by_tags, name='filter_posts_by_tags'),
]