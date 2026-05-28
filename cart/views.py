from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from orders.models import Order, OrderItem

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = request.POST.get('quantity', '1')

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, quantity)
    cart.add(product=product, quantity=quantity)
    messages.success(request, 'Товар добавлен в корзину.')
    return redirect(request.POST.get('next') or 'cart:detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity', '1')

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    cart.add(product=product, quantity=max(0, quantity), override_quantity=True)
    messages.success(request, 'Корзина обновлена.')
    return redirect('cart:detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, 'Товар удален из корзины.')
    return redirect('cart:detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Корзина очищена.')
    return redirect('cart:detail')


@login_required
@require_POST
def cart_checkout(request):
    cart = Cart(request)
    cart_items = list(cart)

    if not cart_items:
        messages.error(request, 'Корзина пуста.')
        return redirect('cart:detail')

    product_ids = [item['product'].id for item in cart_items]

    with transaction.atomic():
        products_map = {
            product.id: product
            for product in Product.objects.select_for_update().filter(id__in=product_ids)
        }

        for item in cart_items:
            product = products_map.get(item['product'].id)
            if not product or not product.is_available:
                messages.error(request, f'Товар "{item["product"].title}" недоступен.')
                return redirect('cart:detail')
            if product.stock < item['quantity']:
                messages.error(
                    request,
                    f'Недостаточно товара "{product.title}" на складе. Доступно: {product.stock}.',
                )
                return redirect('cart:detail')

        order = Order.objects.create(user=request.user, status='new')
        order_items = []
        for item in cart_items:
            product = products_map[item['product'].id]
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price'],
                )
            )
            product.stock -= item['quantity']
            if product.stock <= 0:
                product.is_available = False

        OrderItem.objects.bulk_create(order_items)
        Product.objects.bulk_update(products_map.values(), ['stock', 'is_available'])

    cart.clear()

    email_sent = False
    if request.user.email:
        total = sum(item['total_price'] for item in cart_items)
        lines = [
            f'Здравствуйте, {request.user.username}!',
            '',
            f'Ваш заказ #{order.id} успешно оформлен.',
            'Состав заказа:',
        ]
        for item in cart_items:
            lines.append(f'- {item["product"].title} x {item["quantity"]}')
        lines.extend(['', f'Итого: {total} KZT'])

        try:
            send_mail(
                subject=f'MebelHub: подтверждение заказа #{order.id}',
                message='\n'.join(lines),
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            email_sent = True
        except Exception:
            email_sent = False

    if email_sent:
        messages.success(
            request,
            f'Заказ #{order.id} успешно оформлен. На вашу почту отправлено сообщение о заказе.',
        )
    elif request.user.email:
        messages.success(request, f'Заказ #{order.id} успешно оформлен.')
        messages.warning(request, 'Почтовое сообщение не отправлено. Проверьте настройки SMTP.')
    else:
        messages.success(request, f'Заказ #{order.id} успешно оформлен.')
        messages.warning(request, 'Укажите email в профиле, чтобы получать подтверждения заказов.')

    return redirect('orders:list')
