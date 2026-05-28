from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Brand, Category, Collection, Product
from orders.models import Order


class CartViewsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Диваны', slug='divany')
        brand = Brand.objects.create(name='TestBrand', slug='testbrand')
        collection = Collection.objects.create(title='Test', slug='test')
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            category=category,
            brand=brand,
            collection=collection,
            description='Test description',
            price=Decimal('1000.00'),
            year=2025,
            stock=10,
            is_available=True,
        )

    def test_add_product_to_cart(self):
        response = self.client.post(
            reverse('cart:add', args=[self.product.id]),
            {'quantity': 2, 'next': reverse('cart:detail')},
        )

        self.assertRedirects(response, reverse('cart:detail'))
        session_cart = self.client.session.get('cart', {})
        self.assertEqual(session_cart[str(self.product.id)]['quantity'], 2)

    def test_update_product_quantity(self):
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 1})

        response = self.client.post(reverse('cart:update', args=[self.product.id]), {'quantity': 4})

        self.assertRedirects(response, reverse('cart:detail'))
        session_cart = self.client.session.get('cart', {})
        self.assertEqual(session_cart[str(self.product.id)]['quantity'], 4)

    def test_remove_product_from_cart(self):
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 1})

        response = self.client.post(reverse('cart:remove', args=[self.product.id]))

        self.assertRedirects(response, reverse('cart:detail'))
        session_cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), session_cart)

    def test_checkout_creates_order_and_clears_cart(self):
        user = get_user_model().objects.create_user(username='buyer', password='pass12345')
        self.client.login(username='buyer', password='pass12345')
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 3})

        response = self.client.post(reverse('cart:checkout'))

        self.assertRedirects(response, reverse('orders:list'))
        order = Order.objects.get(user=user)
        self.assertEqual(order.items.count(), 1)
        item = order.items.first()
        self.assertEqual(item.product_id, self.product.id)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.price, self.product.price)
        self.assertEqual(self.client.session.get('cart', {}), {})
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_checkout_requires_authentication(self):
        self.client.post(reverse('cart:add', args=[self.product.id]), {'quantity': 1})

        response = self.client.post(reverse('cart:checkout'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
