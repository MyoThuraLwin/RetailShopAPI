# Generated migration to remove remaining extra columns from product table

from django.db import migrations, models, connection


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_finalize_product_model'),
    ]

    def remove_remaining_columns(apps, schema_editor):
        """
        Remove the remaining extra columns that are still in the database
        """
        with connection.cursor() as cursor:
            # Specific columns that are still in the database
            remaining_columns = [
                'reorder_level',
                'track_inventory',
                'featured_image',
                'slug',
                'custom_user'
            ]
            
            for column in remaining_columns:
                try:
                    cursor.execute(f"ALTER TABLE product DROP COLUMN IF EXISTS {column};")
                    print(f"Successfully removed column: {column}")
                except Exception as e:
                    print(f"Error removing column {column}: {e}")
                    # Column might not exist or have constraints, continue
    
    def reverse_remove_remaining_columns(apps, schema_editor):
        # No reverse operation needed
        pass

    operations = [
        migrations.RunPython(remove_remaining_columns, reverse_remove_remaining_columns),
    ]
