from django.contrib import admin

from .models import Brand, Category, Collection, Color, Feature, Material, Product, ProductImage, Tag


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'brand', 'price', 'stock', 'is_available', 'created_at')
    list_filter = ('category', 'brand', 'is_available', 'year')
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'description', 'cover')}),
        ('Классификация', {'fields': ('category', 'brand', 'collection', 'materials', 'colors', 'tags')}),
        ('Коммерция', {'fields': ('price', 'stock', 'year', 'is_available', 'created_at', 'updated_at')}),
    )

    actions = ['mark_available']

    @admin.action(description='Сделать доступными')
    def mark_available(self, request, queryset):
        queryset.update(is_available=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'hex_code')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    search_fields = ('name', 'value')
