from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        return bool(request.method == 'GET' or (request.user or request.user.is_staff))