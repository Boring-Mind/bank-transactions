from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwner(BasePermission):
    """Custom permission to pass only owner of the object."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsOwnerOrAdmin(BasePermission):
    """Custom permission to pass only owner of the object or admin."""

    def has_permission(self, request, view):
        return (
            IsOwner.has_permission(self, request, view) or
            IsAdminUser.has_permission(self, request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            IsOwner.has_object_permission(self, request, view, obj) or
            IsAdminUser.has_object_permission(self, request, view, obj)
        )
