from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('top_all_time/', views.top, name='top_all_time'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/<int:userid>', views.UserDetailView, name='user-detail'),
]