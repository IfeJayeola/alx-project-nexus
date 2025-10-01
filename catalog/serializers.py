import uuid
from django.db.models import CharField, fields_all
from rest_framework import serializers
from .models import User, Product, Categories, Cart, CartItem, Product, Payment




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

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.product_name", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "price", "quantity", "added_at"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["cart_id", "user", "items", "total", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]

    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "payment_id", "user", "cart", "amount",
            "currency", "chapa_tx_ref", "status",
            "method", "created_at", "updated_at"
        ]
        read_only_fields = ["status", "chapa_tx_ref", "created_at", "updated_at"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['payment_id', 'user', 'cart', 'amount', 'currency', 'status', 'tx_ref', 'created_at', 'updated_at']

        
class AddItemSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField(default=1)


class UpdateItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=0, help_text="Set to 0 to remove the item")
