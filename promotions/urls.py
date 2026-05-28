from django.urls import path

from .views import promotions_list

urlpatterns = [
    path('', promotions_list, name='list'),
]
