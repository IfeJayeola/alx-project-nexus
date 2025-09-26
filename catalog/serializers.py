from django.db.models import CharField, fields_all
from rest_framework import serializers
from .models import User, Product, Categories

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'firstname', 'lastname','role', 'is_active', 'is_staff', 'datejoined']

        password = serializers.CharField(write_only = True, required=True)
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        user = User(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

