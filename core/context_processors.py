from catalog.models import Category


def site_data(request):
    return {
        'menu_categories': Category.objects.all()[:8],
        'site_name': 'MebelHub',
    }
