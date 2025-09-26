from rest_framework import permissions
from .models import Role


class is_Staff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.STAFF
    
class is_StaffOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and request.user == Role.STAFF
        if view.action == 'retrieve':
            if request.user.is_authenticated:
                return True
            return False

    def has_object_permission(self, request, view, obj):
        return request.user = Role.STAFF or obj == request.user

        
class is_StaffOrViewOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == Role.STAFF

class is_SellerOrViewOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == Role.SELLER
