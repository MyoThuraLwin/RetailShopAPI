# Generated migration to finalize product model changes

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_clean_product_columns'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Update product fields to match the simplified model
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Created At'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(
                help_text='Created By', 
                null=True, 
                on_delete=django.db.models.deletion.SET_NULL, 
                related_name='created_products', 
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(help_text='Product Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Product Name', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Price', max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(help_text='Product Code', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Updated At'),
        ),
    ]
