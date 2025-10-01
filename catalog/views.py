import uuid
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import permissions 
from .custom_permissions import is_SellerOrViewOnly, is_Staff, is_StaffOrViewOnly, is_StaffOrSelf
from .models import Categories, User,  Product,  Payment, Cart
from .serializers import UserSerializers, ProductSerializers, CategoriesSerializers, PaymentSerializer, AddItemSerializer, CartSerializer, UpdateItemSerializer
from rest_framework import viewsets, filters
from rest_framework.response import Response
from .sevices.cart_service import CartService
from rest_framework.decorators import action
from .utils import initialize_chapa_payment,  verify_chapa_payment



# Create your views here.
class UserViewSet(viewsets.ModelViewSet):   

    """    
    retrieve:
    Get details of a single user by ID.

    list:
    Get a list of all users

    create:
    Add a new user to the catalog.

    update:
    Update an existing user.

    partial_update:
    Partially update an existing user.

    destroy:
    Delete a user from the catalog.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializers
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return  [is_StaffOrSelf()]
    

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
    permission_classes = [is_SellerOrViewOnly]
    

class CategoriesViewSet(viewsets.ModelViewSet):
    """
    
    retrieve:
    Get details of a single category by ID.

    list:
    Get a list of all categories

    create:
    Add a new category to the catalog.

    update:
    Update an existing category.

    partial_update:
    Partially update an existing category.

    destroy:
    Delete a category from the catalog.
    """

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializers
    permission_classes=[is_StaffOrViewOnly]

class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart, _ = CartService.get_or_create_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="post",
        request_body=AddItemSerializer,
        responses={200: "Item updated successfully"}
    )    @action(detail=False, methods=["post"])
    def add_item(self, request):
        serializer = AddItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        item = CartService.add_item(request.user, product_id, quantity)
        return Response({"message": f"Added {item.quantity} x {item.product.product_name}"})

    @swagger_auto_schema(
        method="post",
        request_body=UpdateItemSerializer,
        responses={200: "Item updated successfully"}
    )
    
    @action(detail=False, methods=["post"])
    def update_item(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        item = CartService.update_item(request.user, product_id, quantity)
        if not item:
            return Response({"message": "Item removed or not found"})
        return Response({"message": f"Updated {item.product.name} to {item.quantity}"})

    @action(detail=False, methods=["post"])
    def clear(self, request):
        CartService.clear_cart(request.user)
        return Response({"message": "Cart cleared"})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset= Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['POST'])
    def create_payment(self, request):
        tx_ref= str(uuid.uuid4())
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)

        amount = cart.get_total_amount


        payment = Payment.objects.create(
            user=user,
            cart=cart,
            tx_ref=tx_ref,
            amount = amount,
            status = 'pending'
        )

        response = initialize_chapa_payment(
            email = user.email,
            amount=amount,
            first_name=user.firstname,
            last_name=user.lastname,
            tx_ref=tx_ref,
            callback_url=f"{settings.BASE_URL}/api/payment/callback/"
        )
        return Response({
            'payment': PaymentSerializer(payment).data,
            'chapa': response
                        })

    
    @action(detail=True, methods=['GET'])
    def verify_payment(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status = 404)
        
        response = verify_chapa_payment(payment.tx_ref)
        if response.get('status') == 'success' and response['data']['status'] == 'success':
            payment.status = 'success'
            payment.save()

#        return Response(PaymentSerializer(payment).data)

        for item in payment.cart.items.all():
            item.product.in_stock -= item.quantity
            item.product.save()
            payment.cart.items.all().delete()
        else:
            payment.status = "failed"
            payment.save()

        return Response(PaymentSerializer(payment).data)
