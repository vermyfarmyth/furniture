from django.urls import path

from .views import my_orders

urlpatterns = [
    path('', my_orders, name='list'),
]
