from rest_framework import permissions


class OwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user.username == obj.username
