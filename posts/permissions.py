from rest_framework.permissions import BasePermission

class IsPostOwner(BasePermission):
    message="You do not have permission to modify this post."
    
    def has_object_permission(self, request, view, obj):
        return obj.author==request.user