from decimal import Decimal

from catalog.models import Product


class Cart:
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(self.SESSION_KEY, {})

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if self.cart[product_id]['quantity'] <= 0:
            del self.cart[product_id]

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session.pop(self.SESSION_KEY, None)
        self.session.modified = True
        self.cart = {}

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(product.id): product for product in products}

        for product_id, item in self.cart.items():
            product = products_map.get(product_id)
            if not product:
                continue
            quantity = int(item['quantity'])
            price = Decimal(item['price'])
            yield {
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
