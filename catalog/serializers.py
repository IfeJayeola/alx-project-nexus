from django.db.models import fields_all
from rest_framework import serializers
from .models import User, Product, Categories

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

