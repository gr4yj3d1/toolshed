from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('inventory', views.inventory, name='inventory'),
    path('profile/<str:username>', views.profile, name='profile'),
]
