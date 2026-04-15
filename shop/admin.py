from django.contrib import admin
from .models import Category, Product, Cart, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

admin.site.register(Cart)
admin.site.register(Order)
