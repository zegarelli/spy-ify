from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('authed/', views.authedView, name='authed'),
    path('top_all_time/', views.top, name='top_all_time'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/plays', views.UserDetailView, name='user-detail'),
    path('plays/', views.UserFreeQueryView, name='plays'),
]