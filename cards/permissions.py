from rest_framework import permissions

from cards.models import User


class CardAccessPermission(permissions.BasePermission):
    """
    Allows user owner to edit an object and company owner to view
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and \
           obj.company.id == request.user.id:
            return True

        return obj.user.id == request.user.id


class UserOnlyPostPermission(permissions.BasePermission):
    """
    Allows post to users with USER role
    """
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.role == User.USER
        return True
