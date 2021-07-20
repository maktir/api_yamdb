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


class ReviewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action == 'create':
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action in ['partial_update', 'destroy']:
            if (request.user == obj.author
                    or request.user.role in ['admin', 'moderator']):
                return True
            return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

