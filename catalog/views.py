from django.shortcuts import render
from .models import Categories, User,  Product, Categories
from .serializers import UserSerializers, ProductSerializers, CategoriesSerializers
from rest_framework import viewsets

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers

