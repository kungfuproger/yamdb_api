from rest_framework import permissions, request


class OwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user.username == obj.username

class AdminOrSuperuserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.username)
        print(request.user.is_authenticated())
        return False
        # return (request.user.is_authenticated() and (request.user.is_admin() or request.user.is_superuser()))
