from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Collection(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Material(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=80, unique=True)
    hex_code = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True)
    materials = models.ManyToManyField(Material, blank=True, related_name='products')
    colors = models.ManyToManyField(Color, blank=True, related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    cover = models.ImageField(upload_to='products/covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def clean(self):
        if self.year < 2000:
            raise ValidationError('Год должен быть не меньше 2000.')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=150, blank=True)


class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    class Meta:
        unique_together = ('product', 'name')

    def __str__(self):
        return f'{self.product}: {self.name}'
