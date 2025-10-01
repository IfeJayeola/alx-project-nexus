from rest_framework.routers import DefaultRouter
from .views import CartViewSet, UserViewSet, ProductViewSet,CategoriesViewSet, PaymentViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'product', ProductViewSet)
router.register(r'cart',CartViewSet, basename='cart')
router.register(r"payments", PaymentViewSet, basename='payments')
