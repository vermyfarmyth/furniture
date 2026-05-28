from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('catalog/', include(('catalog.urls', 'catalog'), namespace='catalog')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),
    path('favorites/', include(('favorites.urls', 'favorites'), namespace='favorites')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('promotions/', include(('promotions.urls', 'promotions'), namespace='promotions')),
    path('support/', include(('support.urls', 'support'), namespace='support')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('api/', include(('api.urls', 'api'), namespace='api')),
]

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
