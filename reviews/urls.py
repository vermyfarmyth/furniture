from django.urls import path

from .views import add_review, my_reviews

urlpatterns = [
    path('', my_reviews, name='list'),
    path('product/<slug:slug>/', add_review, name='add'),
]
