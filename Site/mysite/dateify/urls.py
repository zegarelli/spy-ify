from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('relationship/betsy', views.betsy, name='betsy'),
    path('relationship/dates', views.dates, name='dates')
]