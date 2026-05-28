from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'slug',
            'category',
            'brand',
            'collection',
            'materials',
            'colors',
            'tags',
            'description',
            'price',
            'year',
            'stock',
            'is_available',
            'cover',
        ]
        widgets = {
            'materials': forms.CheckboxSelectMultiple,
            'colors': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple,
            'description': forms.Textarea(attrs={'rows': 4}),
        }
