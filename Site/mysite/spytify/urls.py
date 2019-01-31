from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('authed/', views.authedView, name='authed'),
    path('top_all_time/', views.top, name='top_all_time'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/plays', views.UserPlaysView, name='user-plays'),
    path('track/<trackid>', views.TrackDetailView, name='track-detail'),
]
