from django.urls import path

from .views import list_favorites, toggle_favorite

urlpatterns = [
    path('', list_favorites, name='list'),
    path('toggle/<slug:slug>/', toggle_favorite, name='toggle'),
]
