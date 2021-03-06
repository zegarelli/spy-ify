from django.urls import path
from . import views

urlpatterns = [
    path('post', views.post, name='post'),
    path('posts', views.posts, name='posts'),
    path('api/posts', views.api_posts, name='api_posts')
]