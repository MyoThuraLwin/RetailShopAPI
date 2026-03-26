from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Product(models.Model):
    """
    Simplified model for products in retail shop.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_code = models.CharField(max_length=50, unique=True, help_text="Product Code")
    name = models.CharField(max_length=200, help_text="Product Name")
    description = models.TextField(help_text="Product Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created At")
    updated_at = models.DateTimeField(auto_now=True, help_text="Updated At")
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, related_name='created_products', help_text="Created By")
    
    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product_code']),
            models.Index(fields=['name']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.product_code})"
