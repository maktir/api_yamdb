from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (obj.author == request.user
                or request.method in permissions.SAFE_METHODS):
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        return request.user.role == 'admin'


class IsAdminOrRO(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff



