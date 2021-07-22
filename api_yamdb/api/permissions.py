from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (obj.author == request.user
                or request.method in permissions.SAFE_METHODS):
            return True
        return obj.author == request.user


class AuthAdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_staff)):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (request.user.role == 'admin'
                or request.user.is_staff):
            return True
        return False


class TitlePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        if view.action == 'create':
            if (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.is_staff)):
                return True
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action in ['partial_update', 'destroy']:
            if (request.user.role == 'admin'
                    or request.user.is_staff):
                return True
            return False


class ReviewCommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action in ['partial_update', 'destroy']:
            if (request.user == obj.author
                    or request.user.role in ['admin', 'moderator']
                    or request.user.is_staff):
                return True
            return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
