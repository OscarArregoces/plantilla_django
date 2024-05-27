from rest_framework import permissions


class ViewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        elif request.user.role == "admin":
            return True
        else:
            return obj.created_by == request.user

    def has_permission(self, request, view):
        allowed_views = []

        if (
            request.user.is_superuser
            and request.user.is_staff
            or request.user.role == "admin"
        ):
            return True

        return (
            request.user.is_authenticated and view.__class__.__name__ in allowed_views
        )
