from rest_framework import permissions


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):    
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return(
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return(
                request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser)


class ModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        ):
            return (
                    request.user.is_moderator
                    or request.user.is_admin
                    or (request.user == obj.author)
            )