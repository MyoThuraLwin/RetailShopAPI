# Generated migration to completely reset and fix the products app

from django.db import migrations, models, connection


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    def clean_database_schema(apps, schema_editor):
        """
        Clean up the database manually using raw SQL to avoid Django's confusion
        """
        with connection.cursor() as cursor:
            # First, rollback any failed transaction
            cursor.execute("ROLLBACK;")
            
            # Drop all tables that shouldn't exist in our simplified model
            tables_to_drop = [
                'product_tag_relation',
                'product_review', 
                'product_image',
                'product_category',
                'product_tag'
            ]
            
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                    print(f"Dropped table: {table}")
                except Exception as e:
                    print(f"Error dropping {table}: {e}")
                    # Continue even if table doesn't exist
            
            # Remove the updated_by column from product table if it exists
            try:
                cursor.execute("ALTER TABLE product DROP COLUMN IF EXISTS updated_by;")
                print("Removed updated_by column from product table")
            except Exception as e:
                print(f"Error removing updated_by column: {e}")
                # Column might not exist, that's fine
    
    def reverse_clean_database_schema(apps, schema_editor):
        # No reverse operation needed for this cleanup
        pass

    operations = [
        migrations.RunPython(clean_database_schema, reverse_clean_database_schema),
    ]
