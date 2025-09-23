from django.urls import include, path
from rest_framework import urlpatterns
from .routers import router

urlpatterns = [
    path('', include(router.urls))
]
