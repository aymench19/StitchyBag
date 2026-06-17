from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product,
    ProductImage,
    HeroImage,
    Order,
    OrderItem
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'stock',
        'created_at'
    )
    list_display_links = ('name',)
    list_per_page = 15
    search_fields = ('name',)
    ordering = ('-created_at',)
    inlines = [ProductImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product',
        'quantity',
        'unit_price'
    )


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    @admin.display(description='Statut', ordering='status')
    def status_badge(self, obj):
        color_map = {
            'pending': 'warning',
            'delivered': 'success',
            'canceled': 'danger',
        }
        color = color_map.get(obj.status, 'secondary')
        return format_html(
            '<span class="admin-status-badge admin-status-{}">{}</span>',
            color,
            obj.get_status_display()
        )

    list_display = (
        'reference',
        'first_name',
        'phone',
        'total_price',
        'status_badge',
        'created_at'
    )
    list_display_links = ('reference',)
    list_filter = ('status',)
    ordering = ('-created_at',)
    list_per_page = 15
    date_hierarchy = 'created_at'

    search_fields = (
        'reference',
        'phone',
        'first_name',
        'last_name'
    )

    inlines = [OrderItemInline]


admin.site.register(ProductImage)
admin.site.register(OrderItem)

admin.site.site_header = "Crochet Bags Administration"
admin.site.site_title = "Crochet Bags"
admin.site.index_title = "Gestion de la boutique"