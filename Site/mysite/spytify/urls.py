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
    path('artist/<artistid>', views.ArtistDetailView, name='artist-detail'),
    path('album/<albumid>', views.AlbumDetailView, name='album-detail'),
    path('example_query/', views.example_query, name='example_query'),
    path('user/free_query', views.free_query, name='free_query'),
]
