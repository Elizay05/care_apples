from rest_framework import permissions

class IsAdminRole (permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "Admin"
    
class IsUserRole (permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "User"
    
class IsWomenRole (permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "Women"