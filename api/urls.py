from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.products_api, name='products'),
    path('products/create/', views.product_create_api, name='product_create'),
    path('products/<slug:slug>/', views.product_detail_api, name='product_detail'),
    path('products/<slug:slug>/manage/', views.product_manage_api, name='product_manage'),
    path('categories/', views.categories_api, name='categories'),
    path('reviews/', views.reviews_api, name='reviews'),
    path('favorites/', views.favorites_api, name='favorites'),
]
