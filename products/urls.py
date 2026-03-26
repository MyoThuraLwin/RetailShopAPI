from django.urls import path
from .views import ProductViewSet

urlpatterns = [
    # Product endpoints
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<uuid:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product-detail'),
    path('products/search/', ProductViewSet.as_view({'get': 'search'}), name='product-search'),
]
