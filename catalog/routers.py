from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProductViewSet,CategoriesViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'product', ProductViewSet)
