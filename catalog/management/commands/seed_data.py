from django.core.management.base import BaseCommand

from catalog.models import Brand, Category, Product


class Command(BaseCommand):
    help = 'Seed demo furniture data'

    def handle(self, *args, **options):
        categories = ['Диваны', 'Кровати', 'Столы', 'Шкафы', 'Стулья']
        brands = ['NordWood', 'HomeLine', 'UrbanSeat']

        for name in categories:
            Category.objects.get_or_create(name=name, defaults={'slug': name.lower()})
        for name in brands:
            Brand.objects.get_or_create(name=name, defaults={'slug': name.lower()})

        default_category = Category.objects.first()
        default_brand = Brand.objects.first()

        products = [
            ('divan-oslo', 'Диван Oslo', 'sofa_modern.jpg', 61200),
            ('krovat-luna', 'Кровать Luna', 'bed_scandi.jpg', 63500),
            ('obedennyj-stol-terra', 'Обеденный стол Terra', 'table_dining.jpg', 58800),
            ('kreslo-velvet', 'Кресло Velvet', 'chair_velvet.jpg', 42900),
            ('shkaf-oakline', 'Шкаф OakLine', 'wardrobe_oak.jpg', 74900),
            ('pismennyj-stol-minimal', 'Письменный стол Minimal', 'desk_minimal.jpg', 55100),
            ('stellazh-loft', 'Стеллаж Loft', 'shelf_loft.jpg', 46700),
            ('tumba-tv-smart', 'Тумба TV Smart', 'tv_stand.jpg', 52300),
            ('sofa-bergen', 'Sofa Bergen', 'sofa_bergen.jpg', 67100),
            ('sofa-softcloud', 'Sofa SoftCloud', 'sofa_softcloud.jpg', 69400),
            ('bed-scandi-dream', 'Bed Scandi Dream', 'bed_scandi_dream.jpg', 65900),
            ('bed-nova', 'Bed Nova', 'bed_nova.jpg', 64200),
            ('coffee-table-mono', 'Coffee Table Mono', 'coffee_table_mono.jpg', 39800),
            ('dining-table-oak-prime', 'Dining Table Oak Prime', 'dining_table_oak_prime.jpg', 62300),
            ('wardrobe-softline', 'Wardrobe SoftLine', 'wardrobe_softline.jpg', 77100),
            ('bar-stool-loft', 'Bar Stool Loft', 'bar_stool_loft.jpg', 28900),
        ]

        for i, (slug, title, cover_name, price) in enumerate(products, start=1):
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'category': default_category,
                    'brand': default_brand,
                    'description': 'Демо-товар для каталога.',
                    'price': price,
                    'year': 2025,
                    'stock': 3 + i,
                    'is_available': True,
                    'cover': f'products/covers/{cover_name}',
                },
            )

        self.stdout.write(self.style.SUCCESS('Seed data created.'))
