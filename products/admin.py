from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the simplified Product model.
    """
    list_display = (
        'product_code',
        'name', 
        'price',
        'created_at',
        'created_by'
    )
    list_filter = (
        'created_at',
        'created_by'
    )
    search_fields = (
        'product_code',
        'name',
        'description'
    )
    readonly_fields = (
        'id',
        'created_at',
        'updated_at'
    )
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'product_code',
                'name',
                'description',
                'price'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'created_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Show all products to any authenticated user.
        """
        qs = super().get_queryset(request)
        return qs
    
    def save_model(self, request, obj, form, change):
        """
        Set the created_by field when creating a new product.
        """
        if not obj.pk:  # Only set on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
