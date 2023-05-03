from rest_framework import permissions


class IsOwnerOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return(
            request.user.is_authenticated
            and (
                request.user.moder
                or request.user.admn)
        )

# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return(
#                 request.user.is_superuser
#                 or request.user.is_admin
#             )
    