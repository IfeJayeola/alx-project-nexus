from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from .models import Categories, User,  Product, Categories
from .serializers import UserSerializers, ProductSerializers, CategoriesSerializers
from rest_framework import viewsets, filters

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializers

class ProductViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get details of a single product by ID.

    list:
    Get a list of all products.

    create:
    Add a new product to the catalog.

    update:
    Update an existing product.

    partial_update:
    Partially update an existing product.

    destroy:
    Delete a product from the catalog.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['price']

class CategoriesViewSet(viewsets.ModelViewSet):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers

