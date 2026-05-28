from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('project/', views.project_page, name='project'),
    path('404/', views.error_404_preview, name='error_404_preview'),
]
