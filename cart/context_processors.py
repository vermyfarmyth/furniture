from .cart import Cart


def cart_data(request):
    cart = Cart(request)
    return {
        'cart_total_quantity': len(cart),
    }
