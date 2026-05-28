from django import template

register = template.Library()


@register.filter
def kzt(value):
    return f'{value:,.0f} KZT'.replace(',', ' ')
