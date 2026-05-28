from django.shortcuts import render

from .models import Promotion


def promotions_list(request):
    return render(request, 'promotions/list.html', {'promotions': Promotion.objects.filter(active=True)})
