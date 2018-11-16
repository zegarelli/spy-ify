from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:userid>', views.UserDetailView, name='user-detail'),
]