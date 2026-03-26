# Generated migration to clean up product table columns

from django.db import migrations, models, connection


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_reset_schema'),
    ]

    def clean_product_columns(apps, schema_editor):
        """
        Remove old columns from product table that aren't in our simplified model
        """
        with connection.cursor() as cursor:
            # List of old columns to remove (including the ones you mentioned)
            old_columns = [
                'sku',
                'barcode', 
                'compare_price',
                'cost',
                'stock_quantity',
                'status',
                'condition',
                'is_featured',
                'vendor_id',
                'category_id',
                'weight',
                'dimensions',
                'shipping_weight',
                'shipping_dimensions',
                'meta_title',
                'meta_description',
                'meta_keywords',
                'tax_class',
                'manage_stock',
                'stock_status',
                'backorders_allowed',
                'sold_individually',
                'upsell_ids',
                'cross_sell_ids',
                'purchase_note',
                'total_sales',
                'rating_count',
                'average_rating',
                'review_count',
                'reorder_level',
                'track_inventory',
                'featured_image',
                'slug',
                'custom_user'  # This might be a duplicate/incorrect column
            ]
            
            for column in old_columns:
                try:
                    cursor.execute(f"ALTER TABLE product DROP COLUMN IF EXISTS {column};")
                    print(f"Removed column: {column}")
                except Exception as e:
                    print(f"Error removing column {column}: {e}")
                    # Column might not exist, continue
    
    def reverse_clean_product_columns(apps, schema_editor):
        # No reverse operation needed
        pass

    operations = [
        migrations.RunPython(clean_product_columns, reverse_clean_product_columns),
    ]
