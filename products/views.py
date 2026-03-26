from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Product
from .serializers import ProductSerializer

User = get_user_model()


class ProductViewSet(viewsets.ModelViewSet):
    """
    Simplified ViewSet for Product model with basic CRUD operations.
    All authenticated users can perform CRUD operations.
    """
    queryset = Product.objects.select_related('created_by')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_by']
    search_fields = ['name', 'description', 'product_code']
    ordering_fields = ['name', 'price', 'created_at', 'product_code']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on request parameters"""
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by created_by
        created_by_id = self.request.query_params.get('created_by')
        if created_by_id:
            queryset = queryset.filter(created_by_id=created_by_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search functionality"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Search query is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        products = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(product_code__icontains=query)
        ).distinct()
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
