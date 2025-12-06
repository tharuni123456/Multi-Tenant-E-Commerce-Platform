from rest_framework import permissions

class IsStoreOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "owner")

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "staff")

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "customer")

class TenantSafe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        vendor = getattr(obj, "tenant", None) or getattr(obj, "product", None) and getattr(obj.product, "tenant", None)
        return vendor and request.user.tenant and vendor.id == request.user.tenant.id
